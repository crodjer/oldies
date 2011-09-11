from django_cron import cronScheduler, Job

# This is a function I wrote to check a feedback email address
# and add it to our database. Replace with your own imports

class TestJob(Job):
    run_every = 240
    def job(self):
        print '\nThe test cron job was called.\n'

cronScheduler.register(TestJob)