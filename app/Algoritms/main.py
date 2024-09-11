from .kruskal import Kruskal


class Algorithms(Kruskal):
    pass

if __name__ == "__main__":
    a = Algorithms()
    r = a.kruskal([(1.0, (536, 226), (755, 350)), (0.2, (41, 325), (375, 617)), (0.3, (163, 121), (324, 99)), (0.4, (163, 121), (41, 325)), (3.0, (536, 226), (375, 617))])

    print(r)