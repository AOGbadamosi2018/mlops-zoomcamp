
#this is different from the state bucket
#this is created during the terraform project
resource "aws_s3_bucket" "s3_bucket" {
    bucket = var.bucket_name
    acl = "private"
}



output "name" {
    value = aws_s3_bucket.s3_bucket.bucket
}