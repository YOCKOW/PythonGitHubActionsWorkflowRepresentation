from workflow.Containers import Container, Services
from textwrap import dedent
from unittest import TestCase

class ContaintersTests(TestCase):
  def test_container(self):
    container = Container({
      'image': "swift:latest",
      'env': {
        'MY_ENV': 'MY_VALUE'
      },
      'ports': [80, 8080],
      'volumes': ["my_docker_volume:/volume_mount"],
      'options': "--cpus 1",
    })
    self.assertEqual(container.yaml(), dedent("""\
      image: "swift:latest"
      env:
        MY_ENV: MY_VALUE
      ports:
        - 80
        - 8080
      volumes:
        - "my_docker_volume:/volume_mount"
      options: "--cpus 1"
    """))

  def test_services(self):
    services = Services({
      'nginx': {
        'image': "nginx",
        'ports': ["8080:80"],
        'env': {
          'NGINX_PORT': "80"
        }
      },
      'redis': {
        'image': "redis",
        'ports': ["6379/tcp"]
      }
    })
    self.assertEqual(services.yaml(), dedent("""\
      nginx:
        image: nginx
        env:
          NGINX_PORT: "80"
        ports:
          - "8080:80"
      redis:
        image: redis
        ports:
          - 6379/tcp
    """), services.yaml())
