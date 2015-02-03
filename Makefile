VERSION=0.0.2

all: archive rpm

archive:
	git archive --format=tar HEAD | gzip -c > /tmp/ec2snapshot-$(VERSION).tar.gz

rpm:
	docker-rpmbuild build --output /tmp --spec ec2snapshot.spec --source /tmp/ec2snapshot-$(VERSION).tar.gz centos:centos6
