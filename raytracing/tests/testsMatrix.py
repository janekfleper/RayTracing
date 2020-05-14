import unittest
import envtest # modifies path

from raytracing import *

inf = float("+inf")

# Change this to True if you want to run speed tests
doBenchmark = False


class TestMatrix(unittest.TestCase):
    def testMatrix(self):
        m = Matrix()
        self.assertIsNotNone(m)

    def testMatrixExplicit(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1,
                   frontVertex=0, backVertex=0, apertureDiameter=1.0)
        self.assertIsNotNone(m)
        self.assertEqual(m.A, 1)
        self.assertEqual(m.B, 2)
        self.assertEqual(m.C, 3)
        self.assertEqual(m.D, 4)

    def testMatrixProductMath(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.A, 1 * 5 + 3 * 6)
        self.assertEqual(m3.B, 2 * 5 + 4 * 6)
        self.assertEqual(m3.C, 1 * 7 + 3 * 8)
        self.assertEqual(m3.D, 2 * 7 + 4 * 8)

    def testMatrixProductWithRayMath(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        rayIn = Ray(y=1, theta=45)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.y, 1 * 1 + 2 * 45)
        self.assertEqual(rayOut.theta, 3 * 1 + 4 * 45)

    def testMatrixProductOutpuRayLength(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=2)
        rayIn = Ray(y=1, theta=45, z=1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.z, 2 + 1)

    def testMatrixProductOutputRayAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=2)
        rayIn = Ray(y=1, theta=45, z=1)
        rayOut = m1 * rayIn
        self.assertEqual(rayOut.apertureDiameter, inf)

    def testMatrixProductWithRayGoesOverAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=6, theta=45, z=1)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductWithRayGoesUnderAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=-6, theta=45, z=1)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductRayGoesInAperture(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=-1, theta=45, z=1)
        rayOut = m1 * rayIn
        self.assertFalse(rayOut.isBlocked)

    def testMatrixProductRayAlreadyBlocked(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        rayIn = Ray(y=-1, theta=45, z=1, isBlocked=True)
        rayOut = m1 * rayIn
        self.assertTrue(rayOut.isBlocked)

    def testMatrixProductLength(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVertices(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=10, frontVertex=0, backVertex=10)
        self.assertEqual(m1.frontVertex, 0)
        self.assertEqual(m1.backVertex, 10)

    def testMatrixProductVerticesAllNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertIsNone(m3.frontVertex)
        self.assertIsNone(m3.backVertex)

    def testMatrixProductVerticesSecondNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=10, frontVertex=0, backVertex=10)
        m2 = Matrix(A=5, B=6, C=7, D=8)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesFirstNone(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10, frontVertex=0, backVertex=10)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 10)

    def testMatrixProductVerticesTwoElements(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=5, frontVertex=0, backVertex=5)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10, frontVertex=0, backVertex=10)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 0)
        self.assertEqual(m3.backVertex, 15)

    def testMatrixProductVerticesTwoElementsRepresentingGroups(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, physicalLength=5, frontVertex=1, backVertex=4)
        m2 = Matrix(A=5, B=6, C=7, D=8, physicalLength=10, frontVertex=2, backVertex=9)
        m3 = m2 * m1
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 1)
        self.assertEqual(m3.backVertex, 14)

        m3 = m1 * m2
        self.assertEqual(m3.L, m1.L + m2.L)
        self.assertEqual(m3.frontVertex, 2)
        self.assertEqual(m3.backVertex, 14)

    def testMatrixProductGaussianBeamMath(self):
        m = Matrix(A=1, B=2, C=3, D=4)
        beamIn = GaussianBeam(w=1, wavelength=1)  # q = j\pi
        beamOut = m * beamIn
        q = complex(0, math.pi)
        self.assertEqual(beamOut.q, (1 * q + 2) / (3 * q + 4))

    def testMatrixProductGaussianNotSameRefractionIndex(self):
        m = Matrix(A=1, B=2, C=3, D=4)
        beam = GaussianBeam(w=1, n=1.2)

        with self.assertRaises(UserWarning):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("error")
                m * beam

    def testMatrixProductGaussianBeamWavelengthOut(self):
        m = Matrix(A=1, B=2, C=3, D=4, )
        beamIn = GaussianBeam(w=1, wavelength=1)
        beamOut = m * beamIn
        self.assertEqual(beamOut.wavelength, 1)

    def testMatrixProductGaussianRefractIndexOut(self):
        m = Matrix(A=1, B=2, C=3, D=4, frontIndex=1.33, backIndex=1.33)
        beamIn = GaussianBeam(w=1, wavelength=1, n=1.33)
        beamOut = m * beamIn
        self.assertEqual(beamOut.n, 1.33)

    def testMatrixProductGaussianLength(self):
        m = Matrix(A=1, B=2, C=3, D=4, frontIndex=1.33, physicalLength=1.2)
        beamIn = GaussianBeam(w=1, wavelength=1, z=1, n=1.33)
        beamOut = m * beamIn
        self.assertEqual(beamOut.z, 2.2)

    def testMatrixProductGaussianClippedOverAperture(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1.2, apertureDiameter=2)
        beamIn = GaussianBeam(w=1.1, wavelength=1, z=1)
        beamOut = m * beamIn
        self.assertTrue(beamOut.isClipped)

    def testMatrixProductGaussianInitiallyClipped(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1.2, apertureDiameter=2)
        beamIn = GaussianBeam(w=0.5, wavelength=1, z=1)
        beamIn.isClipped = True
        beamOut = m * beamIn
        self.assertTrue(beamOut.isClipped)

    def testMatrixProductGaussianNotClipped(self):
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1.2)
        beamIn = GaussianBeam(w=1.1, wavelength=1, z=1)
        beamOut = m * beamIn
        self.assertFalse(beamOut.isClipped)

    def testMatrixProductUnknownRightSide(self):
        m = Matrix()
        other = TypeError
        with self.assertRaises(TypeError):
            m * other

    def testApertureDiameter(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=2)
        self.assertTrue(m1.hasFiniteApertureDiameter())
        self.assertEqual(m1.largestDiameter(), 2.0)
        m2 = Matrix(A=1, B=2, C=3, D=4)
        self.assertFalse(m2.hasFiniteApertureDiameter())
        self.assertEqual(m2.largestDiameter(), float("+inf"))

    def testTransferMatrix(self):
        m1 = Matrix(A=1, B=2, C=3, D=4)
        # Null length returns self
        self.assertEqual(m1.transferMatrix(), m1)

        # Length == 1 returns self if upTo >= 1
        m2 = Matrix(A=1, B=2, C=3, D=4, physicalLength=1)
        self.assertEqual(m2.transferMatrix(upTo=1), m2)
        self.assertEqual(m2.transferMatrix(upTo=2), m2)

        # Length == 1 raises exception if upTo<1: can't do partial
        # Subclasses Space() and DielectricSlab() can handle this
        # (not the generic matrix).
        with self.assertRaises(Exception) as context:
            m2.transferMatrix(upTo=0.5)

    def testTransferMatrices(self):
        m1 = Matrix(A=1, B=2, C=3, D=4, frontIndex=2)
        self.assertEqual(m1.transferMatrices(), [m1])
        m1 * GaussianBeam(w=1, n=2)

    def testTrace(self):
        ray = Ray(y=1, theta=1)
        m = Matrix(A=1, B=2, C=3, D=4, physicalLength=1)
        trace = [ray, m * ray]
        self.assertListEqual(m.trace(ray), trace)

    def testTraceNullLength(self):
        ray = Ray(y=1, theta=1)
        m = Matrix(A=1, B=2, C=3, D=4)
        trace = [m * ray]
        self.assertListEqual(m.trace(ray), trace)

    def testTraceBlocked(self):
        ray = Ray(y=10, theta=1)
        m = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10, physicalLength=1)
        trace = m.trace(ray)
        self.assertTrue(all(x.isBlocked for x in trace))

    def testTraceGaussianBeam(self):
        beam = GaussianBeam(w=1)
        m = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        outputBeam = m * beam
        tracedBeam = m.trace(beam)[-1]
        self.assertEqual(tracedBeam.w, outputBeam.w)
        self.assertEqual(tracedBeam.q, outputBeam.q)
        self.assertEqual(tracedBeam.z, outputBeam.z)
        self.assertEqual(tracedBeam.n, outputBeam.n)
        self.assertEqual(tracedBeam.isClipped, outputBeam.isClipped)

    def testTraceThrough(self):
        ray = Ray()
        m = Matrix(A=1, B=2, C=3, D=4, apertureDiameter=10)
        trace = m.traceThrough(ray)
        self.assertEqual(trace, m * ray)

    def testTraceMany(self):
        rays = [Ray(y, theta) for y, theta in zip(range(10, 20), range(10))]
        m = Matrix(physicalLength=1.01)
        traceMany = [[ray, ray] for ray in rays]
        self.assertListEqual(m.traceMany(rays), traceMany)

    def testTraceManyJustOne(self):
        rays = [Ray()]
        m = Matrix(physicalLength=1e-9)
        traceMany = [rays * 2]
        self.assertListEqual(m.traceMany(rays), traceMany)

    def testTraceManyThroughList(self):
        rays = [Ray(y, y) for y in range(10)]
        m = Matrix(physicalLength=1)
        traceManyThrough = m.traceManyThrough(rays)
        for i in range(len(rays)):
            self.assertEqual(rays[i], traceManyThrough[i])

    def testTraceManyThroughOutput(self):
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(y, y) for y in range(10_000)]
            m = Matrix(physicalLength=1)
            m.traceManyThrough(rays, True)
        out = f.getvalue()
        self.assertEqual(out.strip(), "Progress 10000/10000 (100%)")

    def testTraceManyThroughNoOutput(self):
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            rays = [Ray(y, y) for y in range(10_000)]
            m = Matrix(physicalLength=1)
            m.traceManyThrough(rays, False)
        out = f.getvalue()
        self.assertEqual(out.strip(), "")

    def testTraceManyThroughInParallel(self):
        rays = [Ray(y, y) for y in range(10)]
        m = Matrix(physicalLength=1)
        trace = m.traceManyThroughInParallel(rays)
        for i in range(len(rays)):
            self.assertTrue(trace[i] in rays)

    def testTraceManyThroughInParallelNoChunks(self):
        rays = [Ray(y, y) for y in range(10)]
        rays = Rays(rays=rays)
        m = Matrix(physicalLength=1)
        trace = m.traceManyThroughInParallelNoChunks(rays)
        for i in range(len(rays)):
            self.assertEqual(trace[i], rays[i])

    @unittest.skipIf(not doBenchmark, "Not running speed tests.")
    def testTraceManyThroughInParallelNoChunksFaster(self):
        import time
        rays = [Ray(y, y) for y in range(1_000_000)]
        m = Matrix(physicalLength=1)
        timeInitNoParallel = time.perf_counter_ns()
        m.traceManyThrough(rays, False)
        timeInitParallel = time.perf_counter_ns()
        m.traceManyThroughInParallelNoChunks(rays)
        finalTime = time.perf_counter_ns()
        notParallelTime = timeInitParallel - timeInitNoParallel
        parallelTime = finalTime - timeInitParallel
        self.assertTrue(parallelTime < notParallelTime)

    def testPointsOfInterest(self):
        m = Matrix()
        self.assertListEqual(m.pointsOfInterest(1), [])

    def testIsImaging(self):
        m1 = Matrix(A=1, B=0, C=3, D=4)
        self.assertTrue(m1.isImaging)
        m2 = Matrix(A=1, B=1, C=3, D=4)
        self.assertFalse(m2.isImaging)

    def testEffectiveFocalLengthsHasPower(self):
        m = Matrix(1, 2, 3, 4)
        focalLengths = (-1 / 3, -1 / 3)
        self.assertTupleEqual(m.effectiveFocalLengths(), focalLengths)

    def testEffectiveFocalLengthsNoPower(self):
        m = Matrix()
        focalLengths = (inf, inf)
        self.assertTupleEqual(m.effectiveFocalLengths(), focalLengths)

    def testMatrixBackFocalLength(self):
        m = Matrix(1, 2, 3, 4, backVertex=1, physicalLength=1)
        f2 = -1 / 3
        p2 = 0 + 1 + (1 - 1) / 3
        self.assertEqual(m.backFocalLength(), p2 + f2 - 1)

    def testBackFocalLengthSupposedNone(self):
        m = Matrix()
        self.assertIsNone(m.backFocalLength())

    def testMatrixFrontFocalLength(self):
        m = Matrix(1, 2, 3, 4, frontVertex=1, physicalLength=1)
        f1 = -1 / 3
        p1 = 0 - (1 - 4) / 3
        self.assertEqual(m.frontFocalLength(), -(p1 - f1 - 1))

    def testFrontFocalLengthSupposedNone(self):
        m = Matrix()
        self.assertIsNone(m.frontFocalLength())

    def testPrincipalPlanePositions(self):
        m = Matrix(1, 2, 3, 4, physicalLength=1)
        p1 = 0 - (1 - 4) / 3
        p2 = 0 + 1 + (1 - 1) / 3
        self.assertTupleEqual(m.principalPlanePositions(0), (p1, p2))

    def testPrincipalPlanePositionsNoPower(self):
        m = Matrix()
        self.assertTupleEqual(m.principalPlanePositions(0), (None, None))

    def testFocusPositions(self):
        m = Matrix(1, 2, 3, 4, physicalLength=1)
        f1 = -1 / 3
        p1 = 1
        f2 = -1 / 3
        p2 = 1
        self.assertTupleEqual(m.focusPositions(0), (p1 - f1, p2 + f2))

    def testFocusPositionsNoPower(self):
        m = Matrix()
        self.assertTupleEqual(m.focusPositions(0), (None, None))

    def testFiniteForwardConjugate(self):
        m1 = Lens(f=5) * Space(d=10)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

        m1 = Space(d=5) * Lens(f=5) * Space(d=10)
        (d, m2) = m1.forwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)
        self.assertEqual(m2.determinant, 1)

    def testInfiniteForwardConjugate(self):
        m1 = Lens(f=5) * Space(d=5)
        (d, m2) = m1.forwardConjugate()
        self.assertIsNone(m2)
        self.assertEqual(d, float("+inf"))
        self.assertEqual(m1.determinant, 1)

    def testInfiniteBackConjugate(self):
        m = Matrix(A=0)
        self.assertTupleEqual(m.backwardConjugate(), (None, None))

    def testFiniteBackConjugate(self):
        m1 = Space(d=10) * Lens(f=5)
        (d, m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 10)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

        m1 = Space(d=10) * Lens(f=5) * Space(d=5)
        (d, m2) = m1.backwardConjugate()
        self.assertTrue(m2.isImaging)
        self.assertEqual(d, 5)
        self.assertEqual(m1.determinant, 1)
        self.assertEqual(m2.determinant, 1)

    def testMagnificationImaging(self):
        m = Matrix()
        self.assertTupleEqual(m.magnification(), (1, 1))

    def testMagnificationNotImaging(self):
        m = Matrix(B=1)
        self.assertTupleEqual(m.magnification(), (None, None))

    def testMatrixFlipOrientation(self):
        frontVertexInit = 10
        backVertexInit = 20
        frontIndexInit = 1
        backIndexInit = 2
        m = Matrix(frontVertex=frontVertexInit, backVertex=backVertexInit, frontIndex=frontIndexInit,
                   backIndex=backIndexInit)
        m.flipOrientation()
        self.assertTrue(m.isFlipped)
        self.assertEqual(m.backIndex, frontIndexInit)
        self.assertEqual(m.frontIndex, backIndexInit)
        self.assertEqual(m.frontVertex, backVertexInit)
        self.assertEqual(m.backVertex, frontVertexInit)

    def testStrRepresentation(self):
        m = Matrix(C=1)
        strRepresentation = r""" /             \ 
| {0:6.3f}   {1:6.3f} |
|               |
| {2:6.3f}   {3:6.3f} |
 \             /
""".format(1, 0, 1, 1)
        strRepresentation += "\nf={:0.3f}\n".format(-1.0)
        self.assertEqual(str(m).strip(), strRepresentation.strip())

    def testStrRepresentationAfocal(self):
        m = Matrix()
        strRepresentation = r""" /             \ 
| {0:6.3f}   {1:6.3f} |
|               |
| {2:6.3f}   {3:6.3f} |
 \             /
""".format(1, 0, 0, 1)
        strRepresentation += "\nf = +inf (afocal)\n".format(-1.0)
        self.assertEqual(str(m).strip(), strRepresentation.strip())

    def testDielectricInterface(self):
        m = DielectricInterface(n1=1, n2=1.5, R=10)
        self.assertEqual(m.determinant, 1 / 1.5)
        self.assertEqual(m.frontVertex, 0)
        self.assertEqual(m.backVertex, 0)

    def testDielectricInterfaceConvergingSign(self):
        # Positive R is convex for ray
        m = DielectricInterface(n1=1, n2=1.5, R=10)
        outRayDown = m*Ray(y=1,theta=0)
        outRayUp = m*Ray(y=-1,theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testDielectricInterfaceDivergingSign(self):
        # Negative R is concave for ray
        m = DielectricInterface(n1=1, n2=1.5, R=-10)
        outRayUp = m*Ray(y=1,theta=0)
        outRayDown = m*Ray(y=-1,theta=0)

        # Ray is diverging
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickConvergingLens(self):
        # Biconvex
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)
        outRayDown = m*Ray(y=1,theta=0)
        outRayUp = m*Ray(y=-1,theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(m.C < 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickDivergingLens(self):
        # Biconcave
        m = ThickLens(n=1.55, R1=-100, R2=100, thickness=3)
        outRayUp = m*Ray(y=1,theta=0)
        outRayDown = m*Ray(y=-1,theta=0)

        # Ray is diverging
        self.assertTrue(m.C > 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testThickConvergingLensEquivalence(self):
        # Biconvex
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)

        mEquivalent = MatrixGroup()
        mEquivalent.append(DielectricInterface(n1=1, n2=1.55, R=100))
        mEquivalent.append(Space(d=3))
        mEquivalent.append(DielectricInterface(n1=1.55, n2=1.0, R=-100))

        self.assertAlmostEqual(m.A, mEquivalent.A,3)
        self.assertAlmostEqual(m.B, mEquivalent.B,3)
        self.assertAlmostEqual(m.C, mEquivalent.C,3)
        self.assertAlmostEqual(m.D, mEquivalent.D,3)

    def testThickConvergingLensFlip(self):
        # Biconvex
        m1 = ThickLens(n=1.55, R1=200, R2=-100, thickness=3)
        m2 = ThickLens(n=1.55, R1=100, R2=-200, thickness=3)
        m2.flipOrientation()

        self.assertAlmostEqual(m1.determinant, 1,4)
        self.assertAlmostEqual(m2.determinant, 1,4)
        self.assertAlmostEqual(m1.A, m2.A,4)
        self.assertAlmostEqual(m1.B, m2.B,4)
        self.assertAlmostEqual(m1.C, m2.C,4)
        self.assertAlmostEqual(m1.D, m2.D,4)

    def testConvergingCurvedMirror(self):
        # Concave should be positive?
        m = CurvedMirror(R=-100)
        outRayDown = m*Ray(y=1,theta=0)
        outRayUp = m*Ray(y=-1,theta=0)

        # Ray is focussed to focal spot
        self.assertTrue(m.C < 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testDivergingCurvedMirror(self):
        m = CurvedMirror(R=100)
        outRayUp = m*Ray(y=1,theta=0)
        outRayDown = m*Ray(y=-1,theta=0)

        # Ray is diverging
        self.assertTrue(m.C > 0)
        self.assertTrue(outRayDown.theta < 0)
        self.assertTrue(outRayUp.theta > 0)

    def testCurvedMirrorFlip(self):
        # Biconvex
        m1 = CurvedMirror(R=100)
        m2 = CurvedMirror(R=-100)
        m2.flipOrientation()

        self.assertAlmostEqual(m1.determinant, 1,4)
        self.assertAlmostEqual(m2.determinant, 1,4)
        self.assertAlmostEqual(m1.A, m2.A,4)
        self.assertAlmostEqual(m1.B, m2.B,4)
        self.assertAlmostEqual(m1.C, m2.C,4)
        self.assertAlmostEqual(m1.D, m2.D,4)

    def testLensFocalLengths(self):
        m = Lens(f=5)
        self.assertEqual(m.effectiveFocalLengths(), (5, 5))
        self.assertEqual(m.backFocalLength(), 5)
        self.assertEqual(m.frontFocalLength(), 5)

    def deactivated_testThickLensFocalLengths(self):
        m = ThickLens(n=1.55, R1=100, R2=-100, thickness=3)

        self.assertEqual(m.backFocalLength(), 5)
        self.assertEqual(m.frontFocalLength(), 5)

    def testOlympusLens(self):
        self.assertIsNotNone(olympus.LUMPlanFL40X())
        self.assertIsNotNone(olympus.XLUMPlanFLN20X())
        self.assertIsNotNone(olympus.MVPlapo2XC())
        self.assertIsNotNone(olympus.UMPLFN20XW())

    def testThorlabsLenses(self):
        l = thorlabs.ACN254_100_A()
        l = thorlabs.ACN254_075_A()
        l = thorlabs.ACN254_050_A()
        l = thorlabs.ACN254_040_A()
        l = thorlabs.AC254_030_A()
        l = thorlabs.AC254_035_A()
        l = thorlabs.AC254_045_A()
        l = thorlabs.AC254_050_A()
        l = thorlabs.AC254_060_A()
        l = thorlabs.AC254_075_A()
        l = thorlabs.AC254_080_A()
        l = thorlabs.AC254_100_A()
        l = thorlabs.AC254_125_A()
        l = thorlabs.AC254_200_A()
        l = thorlabs.AC254_250_A()
        l = thorlabs.AC254_300_A()
        l = thorlabs.AC254_400_A()
        l = thorlabs.AC254_500_A()

        l = thorlabs.AC508_075_B()
        l = thorlabs.AC508_080_B()
        l = thorlabs.AC508_100_B()
        l = thorlabs.AC508_150_B()
        l = thorlabs.AC508_200_B()
        l = thorlabs.AC508_250_B()
        l = thorlabs.AC508_300_B()
        l = thorlabs.AC508_400_B()
        l = thorlabs.AC508_500_B()
        l = thorlabs.AC508_750_B()
        l = thorlabs.AC508_1000_B()

    def testEdmundLens(self):
        l = eo.PN_33_921()



if __name__ == '__main__':
    unittest.main()
