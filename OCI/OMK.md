https://confluence.oraclecorp.com/confluence/display/OMK/OMK+-+Overview+and+User+Experience#OMKOverviewandUserExperience-Vocabulary

Service development in OCI (and Oracle at large) is a federated process. While several tools, patterns and processes exist to drive common aspects of service development, each service team still bears the full burden of building and operating services, that need to meet the OCI bar around security, compliance, operations, efficiencies, scale and performance.

Each service team runs their own infrastructure, resulting in redundancy of common software installations.
Service teams incur a recurring operational cost of managing their infrastructure.
Service teams have to scale and remove infrastructure based on customer demand.
Recurring monitoring and corrective action of infrastructure, operating system and core process failures.
Each team needs to keep up with the recurring security and regulatory compliance reviews.
Recurring cost of hardening and applying monthly patches to infrastructure.
Integrations with other OCI services (e.g. shipping containerized logs to OCI Logging, configuring dashboards)
Region build which takes away from core service business logic development and toil.

By building on top of OMK, service teams can expect the following business value:
Efficient hardware utilization through optimized bin packing, shape agnostic support and elasticity leading to reduced costs.
Operational efficiencies through centralized infrastructure management.
Reduced time to market by allowing service teams to primarily focus on core business logic development.
Built-in security and compliance.
Out of the box integrations with OCI Logging, OCI Monitoring and Cloud Guard.
Service building primitives to streamline integrations with OCI services such as LBaaS.

There will be different types of OKE clusters in this set, such as (but not limited to):
Shared OKE clusters for OCI Control Planes
Dedicated OKE clusters for OCI Data Planes

OMK team, as the infrastructure administrator, will be solely responsible for managing the OKE clusters in the fleet. They will be in-charge of (not an exhaustive list):
Manage Kubernetes version upgrades
Patch the Kubernetes worker nodes
Maintain enough compute capacity for service teams to deploy and scale their applications

Networking Models
    6.3.3.1. Managed Network Model
In this model, there is no exposed networking into the customer's network. Instead, all access is achieved over the Service Gateways in the OMK and user tenancies. This is aimed at deployments which require no connectivity to endpoints outside of what is offered over the Oracle Services Network (OSN). An example would be an idealized CP deployment, where the components only rely on access to other OCI services such as Kiev, WFaaS, IAM, Object Storage, Compute, etc..,
    6.3.3.2. Bring Your Own Network (BYON) Model
As the name suggests, in this model customers will be able to take charge of the networking setup for the workloads that they deploy to the OMK fleet. By essentially dropping a VNIC in customer specified subnet, the packets flowing in and out of the deployed workloads will be governed by customer's VCN configuration. This would allow them to privately connect to other components in their service, connect to on-premise network (Oracle Corp Network) etc.

6.4. Managed Cluster Namespace Profiles
OMK will use the Cluster Namespace Profiles feature to drive the vending of opinionated Kubernetes namespaces. OMK Fleet tenancy will have a set of cluster namespace profiles available for use and each profile will be applicable for a certain type of workload. 
    
6.5.1. Namespace RBAC
    To support the multi-tenanted clusters, OMK will provision an admin role, as a role binding, for each namespace, bound to that namespace. While this bound role is a cluster role, it will be bound to individual namespaces and will only provide access to resources within the namespace to the IAM group and dynamic groups provided by the customer when creating the Cluster Namespace.

6.5.2. Workload Identity
    This workload resource principal will be mapped to the compartment and tenancy of the Cluster Namespace created by the service team. The workloads running in a namespace will belong to the service team's compartment/tenancy from Identity's perspective.

6.5.3.2. Resource Requests and Limits
    OMK will document the resource quotas associated with each t-shirt size when finalized but service teams should expect limits on the following resources:
    CPU cores
    Memory
    Number of load balancer services
    Number of service accounts
    Number of secrets and config maps
    Number of pods

    Service teams are also allowed to specify the maximum resources a single pod in their namespace can consume through ' omk.oracleiaas.com/max-pod-tshirt-size 
    Note: Only CPU, Memory and LB limits are considered for simplicity. There will be limits on additional resources as well.
    Small: 3 vCPUs, 24 GB memory, 1 load balancer
    Medium: 6 vCPUs, 48 GB memory, 2 load balancers
    Large: 9 vCPUs, 72 GB memory, 3 load balancers

6.5.3.3. Host Patching, Cluster Upgrades, Observability

6.6.5. Shell Access
Service teams will not have SSH access to Kubernetes worker nodes in OMK Fleet. They will not be able get on the nodes, without appropriate privileges, to triage any issues with their pods. Instead, services will have to rely on standard Kubernetes practices to help debug their application. If their running containers have a shell then they could rely on kubectl exec to run diagnostic commands in their pods. Over time, OMK will investigate how it can bring the capability of Ephemeral Containers on OMK Fleet to help streamline operations for services.

5.1.2.1.2. ClusterNamespaceController (CNC)
    Default labels which will always be set by the Cluster Namespace Controller
    "clusternamespace.oraclecloud.com/tenantId": "<OCID>"
    "clusternamespace.oraclecloud.com/compartmentId": "<OCID>"
    "clusternamespace.oraclecloud.com/id": "<OCID>"
    "clusternamespace.oraclecloud.com/profileVersionId": "<OCID>"

CP API->CP Worker->OKE MP

Service Team workloads residing in Cluster Namespaces will get their own isolated compute in the form of Workload Envelopes, an OMK internal construct for managing infrastructure that is isolated from other Cluster Namespaces.
OMK isolates the resources owned by Service Teams through the use of Kubernetes native controls, specifically:
    Kubernetes built-in controls, such as ResourceQuotas, LimitRanges, RBAC, and API Priority and Fairness
    Mutating and Validating Admission Webhooks
    
    The former allows OMK to drive what resources Service Teams are allowed to perform CRUDL access upon, how many resources they are allowed to create, set limits on the amount of infrastructure consumed by resources, and rate-limit access to the resource Kubernetes APIs themselves.
    
    The latter provides a way for OMK to insert custom business logic into the resource processing pipeline of the Kubernetes API, allowing OMK to mutate and validate the contents of resources to meet our isolation requirements.  This includes actions such as modifying workloads so that they run on the correct infrastructure, ensuring Load Balancers are provisioned in the correct subnets, disallowing settings that could affect the scalability/stability of the system, and ensuring that workloads run with secure settings.

     OMK will provision dedicated and isolated infrastructure for each Cluster Namespace using an internal construct called a Workload Envelope.  A Workload Envelope represents an isolated set of infrastructure used by workloads that are considered similar enough and safe enough to share the same infrastructure.  Today, only workloads from the same Cluster Namespace are considered safe to run together, and thus each Cluster Namespace will be dynamically provisioned and assigned its own Workload Envelope.  In the future OMK may support assigning multiple Cluster Namespaces to a single Workload Envelope in cases where infrastructure may be shared to achieve better packing.

     Workload Envelopes will provide the following benefits:
        Blast Radius Protection
        Network Isolation
        Compute Isolation
        A unit of infrastructure that can be targeted for:
        Upgrade
        Scaling
        Co-location of workloads

6. System Design
6.1. Cluster Namespace Isolation via Workload Envelopes
When a Workload Envelope is created, it will be associated with a Cluster Namespace.  This is achieved by placing an annotation with the Workload Envelope name on the Kubernetes Namespace associated with the Cluster Namespace.  This annotation will serve as the link between the Cluster Namespace and the Workload Envelope, and allow OMK Webhooks to enforce assignment of resources (Pods, LB Backends, etc...) to the appropriate Workload Envelope.
Workload Envelopes will be configured via Cluster-scoped Kubernetes Custom Resources.  By placing the Workload Envelope resources in the same persistence store (Kubernetes API) as the Cluster Namespaces that result in their creation, restoration of Clusters from backup will result in a consistent view of the internal desired state.  Any drift between the resources will be handled by OMK controllers as they continuously reconcile.

6.2. **OMK Controller Manager/Cluster Operator**
Cluster Namespaces are expected to provide a level of infrastructure isolation between workloads on OKE Clusters.  This requires Kubernetes configuration, and infrastructure, in the form of Workload Envelopes, to be dynamically provisioned in response to Cluster Namespaces.  It is the job of the OMK Controller Manager (OCM) to manage this dynamic configuration and provisioning, as well as the lifecycle management of the underlying infrastructure.

The OMK Controller Manager consists of several controllers which will operate on the OKE Cluster and OCI infrastructure to manage the dynamic nature of OMK Workloads and help enforce governance.  The OCM consists of the following components:
**Namespace Provisioning Controller (NPC)**:  Responds to Cluster Namespaces provisioned on an OKE Cluster and configures them for use in the OMK Fleet environment.  Part of this provisioning involves the creation of Workload Envelope resources and assigning Cluster Namespaces to their Workload Envelope.
**Workload Envelope Controller (WEC)**:  Configures the OCI resources that back a Workload Envelope and ensure that the resources remain healthy
**Workload Envelope Nanny (WEN)**:  Coordinates asynchronous management of Workload Envelope resources, such as Cluster Autoscaler configuration, compute image upgrade, and abandoned resource cleanup.  It also helps coordinate the rollout of Cluster-wide changes by pacing changes to infrastructure and keeping early failures small.  The WEN is also a controller, but rather than being triggered directly by changes in resources, it is triggered based on artificial events injected periodically to induce resource scans and updates

6.2.2. Namespace Provisioning Controller (NPC)
This controller is responsible for responding to Cluster Namespaces provisioned on an OKE Cluster and configuring them for use in the OMK Fleet environment.  

6.2.3. Workload Envelope Controller (WEC)
This controller is responsible for configuring the OCI resources associated with the Workload Envelope construct.  Workload Envelopes will be defined via Kubernetes Custom Resources, and will be created by the Namespace Provisioning Controller.  In addition to provisioning the infrastructure, it will also ensure that the infrastructure remains consistent with the desired state, including reconciling desired shapes and images for NodePools via the OKE Automated Node Cycling feature and repairing unhealthy Nodes.

6.2.4. Workload Envelope Nanny (WEN)
The Workload Envelope Nanny is responsible for handling the asynchronous configuration of Workload Envelope resources.  This primarily consists of a few different activities:
Updates to existing Workload Envelope resources, outside of shape (handled by the NPC)
Coordination of Node image upgrade for the purposes of patching
Updates to infrastructure (e.g. subnets, label changes, etc...)
Batch configuration of the Cluster Autoscaler
Abandoned resource cleanup

6.3. OMK Admission Webhooks
Kubernetes allows extending the cluster control-plane through Admission webhooks. There are two types of admission webhooks, validating admission webhook and mutating admission webhook, and OMK will leverage both types. OMK will install multiple validating and mutating admission webhooks so that customers can use OMK Fleet in a secure and compliant manner.


OMK - Dynamic Cluster Provisioning
 it is not possible to provision dedicated clusters for customers without a tedious code change and elaborate release plan for every new customer. These complex requirements of scalability and isolation bring the need to dynamically create and manage fleet clusters.
 Normal Scenario:
    Update shepherd code to increase cell count.
    Shepherd release to create cell infrastructure.
    Shepherd release to install OMK operator on the new clusters.
    Shepherd release to install cluster metrics stack on the new clusters.
    Shepherd release to install metrics-server on the new clusters.
    Shepherd release to create cluster attachment.

Management Plane
A new component called Fleet Manager is introduced. Fleet Manager runs on a management cluster in the fleet tenancy and is responsible for scheduling cluster namespaces and managing workload clusters. Fleet Manager is a set of Kubernetes controllers deployed as a custom operator on the management cluster. Fleet Manager itself follows a cellular architecture to reduce blast radius. There are multiple instances of Fleet Managers called Fleet Manager Cells running on separate management clusters. Each fleet tenancy has it's own set of fleet manager cells managing fleets in that tenancy.
CRD                                         Controller                                          Description
-	                        ClusterNamespaceSchedulingController	        Polls for pending lifecycle hooks and schedules cluster namespaces on appropriate cluster attachments.
Cluster	                                 ClusterController	                Top level cluster resource that delegates infrastrure, application and envelope values to child resources. It is also responsible for creating cluster attachments.
ClusterInfrastructure	        ClusterInfrastructureController	            Responsible for managing cluster infrastructure resources.
ClusterApplication	                ClusterApplicationController	        Responsible for creating and managing applications on the cluster.
ClusterWorkloadEnvelope	        ClusterWorkloadEnvelopeController	        Responsible for creating and managing workload envelope values on the cluster.
Watches changes to config map	    ClusterNanny	                        Responsible for keeping a cluster up to date. Updates to clusters are propagated by the nanny in a controlled manner.

Cluster Controller
This controller is responsible for creating the OMK Fleet cell. It reconciles Cluster custom resource. It creates three child resources to delegate creation of infrastructure, applications and workload envelope values for the cluster. Child resources have owner references to the Cluster resource.

Cluster Infrastructure Controller
This controller is responsible for creating cluster infrastructure resources. This includes VCN resources, cluster resources, and DevOps resources.  The ClusterNanny coordinates infrastructure updates by updating the Cluster resource. Once the reconciliation is complete, the controller updates status.observedConfigResourceVersion to match the spec.configResourceVersion. Any future reconciles will exit early if the two values match.

Application Controller
This controller is responsible for installing and updating applications on the cluster. This includes cluster metrics stack, any operators, etc.. The ClusterNanny coordinates application updates by updating the Cluster resource. Once the reconciliation is complete, the controller updates status.observedConfigResourceVersion to match the spec.configResourceVersion. Any future reconciles will exit early if the two values match.

Workload Envelope Values Controllers
This controller is responsible for installing and updating workload envelope values on the cluster. The ClusterNanny coordinates envelope value updates by updating the Cluster resource. Once the reconciliation is complete, the controller updates status.observedConfigResourceVersion to match the spec.configResourceVersion. Any future reconciles will exit early if the two values match.
