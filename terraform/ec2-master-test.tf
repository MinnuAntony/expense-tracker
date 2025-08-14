resource "aws_instance" "k8s_master" {

  ami           = "ami-04f59c565deeb2199"

  instance_type = "t2.large"

  key_name      = "minnunv"

  # No security group specified = uses default

  user_data = file("${path.module}/master_setup-test.sh")

  tags = {

    Name = "Minnu-K8s-Master-test"

  }

}
