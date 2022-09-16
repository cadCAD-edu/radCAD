from radcad.backends import Executor
import radcad.core as core

import multiprocessing


class ExecutorMultiprocessing(Executor):
    def execute_runs(self):
        with multiprocessing.get_context("spawn").Pool(
                processes=self.engine.processes
            ) as pool:
            result = pool.map(
                core.multiprocess_wrapper,
                self.engine._run_generator,
            )
            pool.close()
            pool.join()
        return result
