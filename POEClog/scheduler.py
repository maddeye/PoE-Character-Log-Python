import datetime

from logging import Logger
from traceback import format_exc

from schedule import Job, Scheduler


class SafeScheduler(Scheduler):
    def __init__(self, logger: Logger, rerun_immediatly: bool = True):
        self.logger = logger
        self.rerun = rerun_immediatly

        super().__init__()

    def _run_job(self, job: Job):
        try:
            super()._run_job(job)
        except Exception:
            self.logger.error(f"Error while {next(iter(job.tags))}...\n{format_exc()}")
            job.last_run = datetime.datetime.now()

            if not self.rerun:
                job._schedule_next_run()
