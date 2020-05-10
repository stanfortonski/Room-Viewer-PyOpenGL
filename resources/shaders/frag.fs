#version 330 core

out vec4 fragColor;

in vec3 normal;
in vec3 fragPos;

struct Material
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

struct PointLight
{
    vec3 position;
    float constant;
    float linear;
    float quadratic;
    vec3 diffuse;
    vec3 ambient;
    vec3 specular;
};

const int DISCS_PCF_AMOUNT = 20;
const vec3 DISCS_PCF[DISCS_PCF_AMOUNT] = vec3[](
   vec3(1, 1, 1), vec3(1, -1, 1), vec3(-1, -1, 1), vec3(-1, 1, 1),
   vec3(1, 1, -1), vec3(1, -1, -1), vec3(-1, -1, -1), vec3(-1, 1, -1),
   vec3(1, 1, 0), vec3(1, -1, 0), vec3(-1, -1, 0), vec3(-1, 1, 0),
   vec3(1, 0, 1), vec3(-1, 0, 1), vec3(1, 0, -1), vec3(-1, 0, -1),
   vec3(0, 1, 1), vec3(0, -1, 1), vec3(0, -1, -1), vec3(0, 1, -1)
);

uniform vec3 viewPos;
uniform float farPlane;
uniform vec3 lightPos;
uniform samplerCube depthMap;
uniform Material material;
uniform PointLight light;

vec3 calcPointLight(PointLight light, vec3 normal, vec3 viewDir, float shadow);
float shadowCalculation(PointLight light);

void main()
{
    PointLight light;
    light.position = lightPos;
    light.ambient = vec3(0.2);
    light.diffuse = vec3(0.75);
    light.specular = vec3(0.1);
    light.constant = 1.0;
    light.linear = 0.001;
    light.quadratic = 0.001;

    vec3 norm = normalize(normal);
    vec3 viewDir = normalize(viewPos - fragPos);
    float shadowVal = shadowCalculation(light);
    vec3 result = calcPointLight(light, norm, viewDir, shadowVal);
    fragColor = vec4(result, 1.0);
}

float shadowCalculation(PointLight light)
{
    const float bias = 0.15;

    vec3 LightToFragDir = fragPos - light.position;
    float currentDepth = length(LightToFragDir) - bias;
    float viewDistance = length(viewPos - fragPos);
    float diskRadius = clamp(viewDistance / farPlane, 0.009, 0.01);

    float shadow = 0.0;
    for (int i = 0; i < DISCS_PCF_AMOUNT; ++i)
    {
        float closestDepth = texture(depthMap, LightToFragDir + DISCS_PCF[i] * diskRadius).r;
        closestDepth *= farPlane;
        if (currentDepth > closestDepth)
            shadow += 1.0;
    }
    shadow /= float(DISCS_PCF_AMOUNT);
    return shadow;
}

vec3 calcPointLight(PointLight light, vec3 normal, vec3 viewDir, float shadow)
{
    vec3 lightDir = normalize(light.position - fragPos);

    float diff = max(dot(normal, lightDir), 0.0);
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material.shininess*0.2);

    float distances = length(light.position - fragPos);
    float weakening = 1.0 / (light.constant + light.linear * distances + light.quadratic * pow(distances, 2.0));

    vec3 ambient = light.ambient * weakening;
    vec3 diffuse = light.diffuse * diff * weakening;
    vec3 specular = light.specular * spec * weakening;
    return (ambient + (1.0 - shadow) * (diffuse + specular)) * (material.diffuse + material.specular);
}