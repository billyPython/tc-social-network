create-social::
	sh -c "sudo docker-compose up --no-start"
	sh -c "sudo docker start social-network"
	sh -c "sudo docker start postgres-social"

migrate-social::
	sh -c "sudo docker exec -it social-network python manage.py migrate"

.PHONY=bot-social
bot-social::
	sh -c "sudo docker exec -it social-network python manage.py bot --data /social-network/social_bot/data/data.json"