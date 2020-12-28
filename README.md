Solution Proposed:



############################################################
REQUIREMENT 1: CREATING REST API

Return Python code using flask and created  the GET api

I have used Python flask core module for development of the same.


1. http://18.223.120.111:5000/hello -- This is giving simple response (Working from browser)

Corresponding main.py is attached

Way to test the code is:

python3 main.py


################################################################
REQUIRMENT 2: CONTAINIERIZATION OF APPLICATION AND TEST IT WITH DOCKER CONTAINER (LOCAL)



2. It is containerized using Dockerfile code which is attached.

3. Run the command to create image, please ensure docker is installed and service is running

docker build -t w2oimage . (. represents the current directory)

4. Run following command to create container using the image

 docker run -t -i -d -p 8080:8080 w2oimage 

5.  Access the application url on http://<instanceip>:8080/hello
In my case it is http://18.223.120.111:8080/hello


###############################################################

REQUIRMENT 3: DEPLOY ON THE KUBERNETES CLUSTER

6. We need to create kubernetes object using the following command

kubectl create deployment w2orestapi --image=wtoimage --dry-run=client -o yaml > restapideploy.yaml

restapideploy.yaml is attached

7. Please note we can change the replicas, namespace and other parameters

8. Change the imagePullPolicy : IfNotPresent ( As in the demo we are using the local image)

9. Created the AWS EKS cluster manually and tested the same, used following commands to integrate with EKS cluster and deployment

aws eks --region us-east-2 update-kubeconfig --name w2oTFcluster

10. Expose the POD and create the service so that application is accessible from outside.

################################################################

CONSIDERATION REQUIREMENT FOR PRODUCTION

1. Deployment is fully automated using pipeline, as in actual scenario, developer will commit code to repo, pipeline will create new image,
test it out, push the new image and deploy it.

2. For High Availability we will have three replicas of application running, which is running across different nodes.
Also, we will enable Horizontal Pod Scaler(HPA) based on metrics like CPU, memory and essentially it will scaleup application automatically.

3. Logging will be enabled with cloudwatch by default, but we can also have some log agreggation tool configured like ELK, SPLUNK, which will push
the data centrally.

4. We will use volumes to write logs, this will ensure that we dont lose logs even if the POD terminates.

##########################################################################

REQUIRMENT 4- BONUS QUESTION -- TERRAFORM CODE TO CREATE EKS CLUSTER

1. Entire terraform script is attached and tested, it created the cluster well.

2. Terraform output was below:



cluster_endpoint = "https://C954A747A319777A7179AAA46D889995.gr7.us-east-2.eks.amazonaws.com"
cluster_id = "w2oTFcluster"
cluster_name = "training-eks-K3ANsFSK"
cluster_security_group_id = "sg-083b33bea9bb2a456"
config_map_aws_auth = [
  {
    "binary_data" = tomap(null) /* of string */
    "data" = tomap({
      "mapAccounts" = <<-EOT
      []

      EOT
      "mapRoles" = <<-EOT
      - "groups":
        - "system:bootstrappers"
        - "system:nodes"
        "rolearn": "arn:aws:iam::524036990776:role/w2oTFcluster2020122508051710250000000c"
        "username": "system:node:{{EC2PrivateDNSName}}"

      EOT
      "mapUsers" = <<-EOT
      []

      EOT
    })
    "id" = "kube-system/aws-auth"
    "metadata" = tolist([
      {
        "annotations" = tomap(null) /* of string */
        "generate_name" = ""
        "generation" = 0
        "labels" = tomap({
          "app.kubernetes.io/managed-by" = "Terraform"
          "terraform.io/module" = "terraform-aws-modules.eks.aws"
        })
        "name" = "aws-auth"
        "namespace" = "kube-system"
        "resource_version" = "880"
        "self_link" = "/api/v1/namespaces/kube-system/configmaps/aws-auth"
        "uid" = "57c83f17-bffa-47aa-aea7-aeb3505f72ff"
      },
    ])
  },
]
kubectl_config = <<EOT
apiVersion: v1
preferences: {}
kind: Config

clusters:
- cluster:
    server: https://C954A747A319777A7179AAA46D889995.gr7.us-east-2.eks.amazonaws.com
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJd01USXlOVEE0TURBeU1sb1hEVE13TVRJeU16QTRNREF5TWxvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTHZqCjZTNGJEOVh2NU8rU0tvZEtsMEwvQWZYbVRpRTNreDg0Y1ZlTXVkMG16Z2dNa21nVW1ReThWNVZtMG9sbUVlVzIKQXNwb1NkenI2RlF0MVdISU5FKzJtQWN1WmYwcis5Qkh4L2FWYkVKMjRIL1pYNlFiV0c3SzFPNndvaVBpWGRSZQpRbFB4Z3R2aVE2YnAwTkZCWlMxeHB6QlJ0b1lzWnd5cHh1TTVnajJFZFhWbUZkV21PLy9BOHlMc25JTGVoT05uCkRTcUUwUEdKVHVxZmFETDh0TERFWU1Oa3ZmNHpxVnlIMzJORnhXM2J4dkNNN2VKZUUrRzNUZm1UaFBGNm84Q3AKczdHNnF4Z2tvSEJiZjFWSGE1Z2x6bXV5UTJQL2JZZmxqdkxQWC9aNUlUclpQZElrNHJIcVdjOTMrVlc3bFpkUApxb3dSUCtvWXVjMWJCUmJuZFVzQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFDZG1JZEpwU0Z6YitjcWpYVHc2aFg1NjRyMVUKMUw4bTJJT2p3b3p1Vld6ZTJwUzFobDMxTDhDWXBpSGdwcm1ySjJmbkFsVDFqK1dpOS9VUlVTdHBYemU4M1c4bAp3Zm1oVUVaRTMzaUhTMGs0VU1oK2I2cFJPeHE3OVRmd001ZDdMZ0FySXNQWU9jZC81WktSeFpSUzJWUFZXaThICno2L09Tb1R1Mis2Z3FxdldqckZCWFNGbFdhUDBPV1RyaUFhQmhudFNwRys2dkJ3QkVsdEVxdlp2YWxnV2kzUjUKNldOd25lZjlCVkF2d002dHlzZlBrU3NKU2JKNFdtNGFGYnZmVjBuMDlIcjNpU040S3NqUUt3Sjkwd2VVZGJNegpSTnZOcTJudXN4c1RLdEhBclk1bzYrK1NpdGl5bWxyYkxtZ1hkT0xaSTVWOWFhdWJrTExyak9HWDd1TT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
  name: eks_w2oTFcluster

contexts:
- context:
    cluster: eks_w2oTFcluster
    user: eks_w2oTFcluster
  name: eks_w2oTFcluster

current-context: eks_w2oTFcluster

users:
- name: eks_w2oTFcluster
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      command: aws-iam-authenticator
      args:
        - "token"
        - "-i"
        - "w2oTFcluster"

EOT
region = "us-east-2"



