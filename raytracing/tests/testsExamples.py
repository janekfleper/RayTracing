import envtest  # modifies path
import subprocess
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import patches, transforms
from unittest.mock import Mock, patch

from raytracing import *

class TestExamples(envtest.RaytracingTestCase):

    def testExamplesArePresent(self):
        import raytracing.examples as ex
        self.assertTrue(len(ex.all) > 0)

    # @patch("matplotlib.pyplot.show", new=Mock())
    def testExamplesRun(self):
        import raytracing.examples as ex
        for ex in ex.all:
            self.assertTrue(len(ex["title"])!=0)
            self.assertTrue(len(ex["sourceCode"])!=0)

    def testExamplesHaveSrcCode(self):
        import raytracing.examples as ex
        for ex in ex.all:
            self.assertTrue(len(ex["sourceCode"])!=0)

    def testExamplesHaveBmpSrcCode(self):
        import raytracing.examples as ex
        for ex in ex.all:
            self.assertIsNotNone(ex["bmpSourceCode"])

    @envtest.skipUnless(envtest.performanceTests, "Skipping long performance tests")
    def testScriptsRun(self):
        import raytracing.examples as ex
        for scripts in ex.allLong:
            err = os.system('{0} {1}'.format(sys.executable, scripts["path"]))
            self.assertTrue(err == 0)
    


if __name__ == '__main__':
    envtest.main()
