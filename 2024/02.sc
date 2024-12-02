def parseReports(input: String): List[List[Int]] =
    input
        .trim
        .linesIterator
        .map(l => l.split("\\s").map(_.toInt).toList)
        .toList


def isSafe(report: List[Int]): Boolean =
    val offsets = report.sliding(2).collect { case List(a, b) => a - b }.toList
    (offsets.forall(_ > 0) || offsets.forall(_ < 0)) && (offsets.forall(_.abs <= 3))


def isSafeDampened(report: List[Int]): Boolean =
    isSafe(report) || (0 until report.length).exists(i => isSafe(report.patch(i, Nil, 1)))


val exampleReports = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def example(): Unit =
    val reports = parseReports(exampleReports)
    assert(reports.map(isSafe).count(identity) == 2)
    assert(reports.map(isSafeDampened).count(identity) == 4)


example()

val input = scala.io.Source.fromFile("2024/02.input").mkString
val reports = parseReports(input)

println(reports.map(isSafe).count(identity))
println(reports.map(isSafeDampened).count(identity))