import luigi
import shutil

class TaskA(luigi.Task):
    # Define multiple output parameters that will be passed to the next task
    output_variable_1 = luigi.Parameter()
    output_variable_2 = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("output_a.txt")

    def run(self):
        # Perform some processing and write the results to the output file
        with self.output().open('w') as f:
            f.write(f"{self.output_variable_1}, {self.output_variable_2}")

class TaskB(luigi.Task):
    # Define multiple input parameters to receive values from the previous task
    input_variable_1 = luigi.Parameter()
    input_variable_2 = luigi.Parameter()
   
    def requires(self):
        a = ''
        b = self.input_variable_1
        return TaskA(output_variable_1=a, output_variable_2=b)

    def output(self):
        return luigi.LocalTarget("output_b.txt")

    def run(self):
        # Use the input variables received from the previous task
        with self.output().open('w') as f:
            f.write(f"{self.input_variable_1}, {self.input_variable_2}")
        a = 'asd'
        b = 'asdw'
if __name__ == '__main__':
    luigi.build([TaskB('a','d')], local_scheduler=True)
