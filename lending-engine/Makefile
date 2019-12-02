clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
run:
	python manage.py run
init:
	python manage.py init

investor-worker:
	celery worker -A task.worker.celery --loglevel=info --autoscale=4,2 -Q investor -n investor@%h

utility-worker:
	celery worker -A task.worker.celery --loglevel=info --autoscale=4,2 -Q utility -n utility@%h

va-worker:
	celery worker -A task.worker.celery --loglevel=info --autoscale=4,2 -Q virtual_account -n virtual_account@%h

investment-worker:
	celery worker -A task.worker.celery --loglevel=info --autoscale=4,2 -Q investment -n investment@%h

transaction-worker:
	celery worker -A task.worker.celery --loglevel=info --autoscale=4,2 -Q transaction -n transaction@%h
periodic-worker:
	celery worker -A task.worker.celery --loglevel=info --autoscale=4,2 -Q periodic -n periodic@%h
beat:
	celery beat -A task.worker.celery --loglevel=info
