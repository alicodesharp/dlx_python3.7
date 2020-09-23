import sys
from functools import reduce
import ksubsetlex
import combfuncs
import DLX_Class


class DesignDLX(DLX_Class.DLX):

    def __init__(self, t, v, k, fixings=True):
        self.t = t
        self.v = v
        self.k = k

        """
        Bir sonraki satır, all fonksiyonu ile v elemanlı kümeden k elemanlı alt kümelerini veriyor. Fonksiyonda son
        olarak return yerine yield kullanılmış, yani generator oluşturulmuş, bunun sebebi ise memory den yer kazanmak.
        """

        columns = list(ksubsetlex.all(v, t))

        """
        Belirli bir alt kümeyi, demeti veya permütasyonu depolamanın birden çok yolu vardır, ancak daha da önemlisi, bu 
        nesnelerin tüm koleksiyonu üzerinde bir bilgi listesinin nasıl depolanacağıdır. Buradaki yöntemde ise her bir 
        nesneye bir dizi konumu atamamızı sağlayan ranking fonksiyonunu kullanıyoruz. Ardından, unranking ile bu süreci
        tersine çeviriyoruz. Bunu yapabiliyor olmamızın sebebi ise [N] 'nin alt kümeleri ile ilk 2^n tamsayıları
        arasında bir eşleştirme(izomorfizma) bulunmasıdır.
        
        Kaynak:
        https://computationalcombinatorics.wordpress.com/2012/09/10/ranking-and-unranking-of-combinations-and-permutations/
        """

        """
        createLookup fonksiyonunda bizim ilgilendiğimiz kısım integer değerlerinin verildiği kısım.
        ör: v=7, k=3, \lambda=1 durumunda, createLookup(S) 7 döndürmeli.
        
        T ler ise dönen k elemanlı alt kümeler.
        t = 2 , bizim BIBDler için.
        """
        rows = [[ksubsetlex.rank(v, T) for T in ksubsetlex.all(combfuncs.createLookup(S), t)] for S in ksubsetlex.all(v, k)]

        """
        Aşağıdaki inherite ettiğimiz asıl DLX - Dancing Link, X algoritmasıdır. Başlangıç parametreleri
        olarak k-subset leri alır. __init__(self, columns, rows=None, rowNames=None) şeklinde initializator'u var.
        
        ****Class içerisinde tanımlanan methodlar****
        
        _cover(column)
        _uncover(column)
        _solve(self, depth, columnselector, columnselectoruserdata, statistics)
        solve(self, columnselector=smallestColumnSelector, columnselectoruserdata=None)
        printSolution(self, solution)
        getRowList(self, row)
        smallestColumnSelector(self, _)
        leftmostColumnSelector(self, _)
        unuseRow(self, rowindex)
        useRow(self, rowindex)
        appendRow(self, row, rowName=None)
        appendRows(self, rows, rowNames=None)
        
        """
        DLX_Class.DLX.__init__(self, [(c, DLX_Class.DLX.PRIMARY) for c in columns])

        self.rowsByLexOrder = self.appendRows(rows)

        self.fixedBlocks = []
        if fixings:
            i = 0
            block = list(range(0, t - 1)) + [0] * (k - t + 1)
            while (i + 1) * k - i * t + (i - 1) < v:
                block[t - 1:] = range(i * k - (i - 1) * t + (i - 1), (i + 1) * k - i * t + i)

                r = ksubsetlex.rank(v, block)
                self.fixedBlocks.append(r)
                self.useRow(self.rowsByLexOrder[r])

                i += 1

            block[t - 2:] = [i * k - (i - 1) * t + (i - 1) for i in range(k - t + 2)]
            r = ksubsetlex.rank(v, block)
            self.fixedBlocks.append(r)
            self.useRow(self.rowsByLexOrder[r])

    def Solution(self, solution):
        """
        Bir sonraki satırda:
        lambda x,y: x+y aslında f(x,y) = x+y şeklinde bir fonksiyon üretir.
        Daha sonra, reduce fonksiyonu ise f(x,y) fonksiyonundan sonra verilen liste elemanları için benzer
        işlemi uygular.

        Örneğin f(x,y) = x+y iken [1,2,3] listesi devreye girer ise,
        f(f(1,2),3) = f(3,3) = 6 sonucunu alırız.
        """
        return list(set(reduce(lambda x, y: x + y, self.getRowList('{}'.format(i for i in solution)), [])))


"""
Python'da modüller çağrıldığında otomatik olarak çalışmasın diye if __name__ == "__main__": kullanılıyor.
"""
if __name__ == "__main__":
    if len(sys.argv) not in range(4, 7):
        print("Usage: %s t v k [use_fixings=T/*F*] [print_designs=T/*F*]" % sys.argv[0])
        exit(1)

    # Use Psyco to speed things up if it is available.
    try:
        import psyco

        psyco.full()
    except ImportError:
        pass

    fixFlag = False

    printFlag = False

    (t, v, k) = map(int, sys.argv[1:4])
    if len(sys.argv) > 4:
        fixFlag = (sys.argv[4] == 'T')
    if len(sys.argv) > 5:
        printFlag = (sys.argv[5] == 'T')

    d = DesignDLX(t, v, k, fixFlag)

    designList = list(d.solve())

    print("*** DONE ***")
    print("Number of designs found: %d" % len(designList))
    if printFlag:
        for design in designList:
            d.printSolution(design)
    print("Nodes per level:", d.statistics.nodes)
    print("Updates per level:", d.statistics.updates)
