class { '::rabbitmq':
  service_manage    => true,
  port              => '5672',
  version           => '3.1.5-1',
}
