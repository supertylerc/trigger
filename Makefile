version=0.0.1

clean:
				@rm -rf *.egg-info
				@rm -rf .tox/

install:
				@pip install -U .

.PHONY: test
test:
				@docker run --rm -v `pwd`:/src supertylerc/trigger-client-build -e py27

lint:
				@docker run --rm -v `pwd`:/src supertylerc/trigger-client-build -e lint
