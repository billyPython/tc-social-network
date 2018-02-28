clean-pyc::
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

.PHONY=create-social
create-social::
	sh -c "sudo docker-compose up --no-start"

.PHONY=start-social
start-social::
	sh -c "sudo docker start social-network"
	sh -c "sudo docker start postgres-social"

.PHONY=migrate-social
migrate-social::
	sh -c "sudo docker exec -it social-network python manage.py migrate"