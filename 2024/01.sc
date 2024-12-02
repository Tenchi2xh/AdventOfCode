def parseLists(input: String): (List[Int], List[Int]) =
    input
        .trim
        .linesIterator
        .map(_.split("\\s+"))
        .map { case Array(a, b) => (a.toInt, b.toInt) }
        .toList
        .unzip


def distance(list0: List[Int], list1: List[Int]): Int =
    list0
        .sorted
        .zip(list1.sorted)
        .map { case (a, b) => (a - b).abs }
        .sum


def similarity(list0: List[Int], list1: List[Int]): Int =
    list0
        .map(a => a * list1.count(_ == a))
        .sum


val exampleLists = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def example(): Unit =
    val (l0, l1) = parseLists(exampleLists)
    assert(distance(l0, l1) == 11)
    assert(similarity(l0, l1) == 31)


example()

val input = scala.io.Source.fromFile("2024/01.input").mkString
val (l0, l1) = parseLists(input)

println(distance(l0, l1))
println(similarity(l0, l1))
