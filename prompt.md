# Mastering the Art of Prompting

A prompt is the instruction or question you give to an AI model. Think of it like giving directions to a driver - the clearer and more specific your instructions, the better your destination (results). Good prompts guide the AI to produce the responses you actually want.

```ascii
    +----------------+
    |     Prompt     | ← Your question or instructions
    +--------+-------+
            |
            v
    +----------------+
    |      AI        | ← Processes your instructions
    |     Model      |
    +--------+-------+
            |
            v
    +----------------+
    |    Response    | ← The output you receive
    +----------------+
```

## Effective Prompt Fundamentals

### Clarity

**Definition:** A clear prompt leaves no room for misinterpretation, just like clear directions prevent wrong turns. It uses precise, specific language instead of vague terms, presents information in a logical, organized structure, and directly states exactly what you want the AI to do.

❌ "Help with my terraform code."

✅ "Explain how to ignore and skip a terraform module using a for_each feature."


### Specificity

**Definition:** Specific prompts include details that narrow the focus to exactly what you need, similar to searching with exact keywords instead of general terms. They include relevant background context, specify parameters like format, length, tone, or audience, and set clear boundaries or constraints for the response. Using information dense action words (like CREATE, UPDATE, MOVE, MIRROR) helps clearly communicate your intent.


| Keyword | Icon | Purpose | Example Usage |
|---------|------|---------|---------------|
| CREATE | 🏗️ | Generate new resources or components | "CREATE a new Azure Function App with premium tier hosting" |
| UPDATE | 🔄 | Modify existing configurations | "UPDATE the connection strings in all App Service instances" |
| COPY/MIRROR | 📋 | Duplicate or replicate resources | "MIRROR the production environment to staging" |
| DEPLOY | 🚀 | Push to specific environments | "DEPLOY the updated Bicep templates to all regions" |
| DELETE | 🗑️ | Remove resources or configurations | "DELETE all unused storage accounts in the dev subscription" |
| ANALYZE | 🔍 | Review and provide insights | "ANALYZE the ARM template for security best practices" |

🤔 _General:_ "Write an Azure Bicep template."

🎯 _Specific:_ "CREATE an Azure Bicep template that provisions an AKS cluster (Standard_D2s_v3 nodes) with a managed identity, Azure Container Registry integration, and Azure Monitor enabled. Include RBAC configuration and network policies. The template should use modules for reusability and include parameter descriptions."

More Examples:
```text
❌ "Help me with my Terraform state in Azure."
✅ "MOVE the Azure SQL Database resource from terraform.tfstate to a new state file named 'database.tfstate' in the Azure Storage backend"

❌ "Fix my Bicep template."
✅ "UPDATE the SKU and capacity settings in the Azure App Service Plan module to scale to P2v3 with 3 instances and enable zone redundancy"

❌ "Copy this to another region."
✅ "MIRROR the existing Azure Application Gateway configuration from East US to West US 2, including all SSL certificates, WAF policies, and backend pools using Terraform workspaces"

❌ "Check my Azure resources."
✅ "ANALYZE the Azure Virtual Network configuration in my Bicep template for subnet overlapping, NSG rules conflicts, and service endpoint misconfigurations"
```


### Context Inclusion

**Definition:** Context gives the AI background information to frame its response, like telling a friend about prior conversations before asking for advice. Effective context includes relevant history or facts, explains why you're asking or what goal you're trying to achieve, and identifies who will use the information or what their knowledge level is.

⛔ _Without Context:_ "Why isn't my service accessible in Kubernetes?"

📝 _With Context:_ "I'm trying to expose a service in kubernetes. The pods are running but external users can't access the API. Can you help me understand if there are any issues with this service configuration that might prevent external access? Here's my current service configuration:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
  labels:
    app: api
    environment: production
spec:
  type: LoadBalancer
  selector:
    app: api
    environment: production
  ports:
    - name: http
      port: 80          # External port
      targetPort: 8080  # Container port
      protocol: TCP
  # Optional: Specify which IP ranges can access the service
  loadBalancerSourceRanges:
    - "0.0.0.0/0"
```

---

> __🤔 Go Deeper__ --> [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)

---

# Practical Demonstration

- [Prompt Chaining](https://github.com/danielscholl/prompt-chains)
- [POM File Metadata Prompt](https://gist.github.com/danielscholl/6b7579a9d5aab8ea231210c3f8c42cd7)
