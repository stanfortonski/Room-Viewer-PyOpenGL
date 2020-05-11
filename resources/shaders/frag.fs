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
    vec3 diffuse;
    vec3 ambient;
    vec3 specular;
    float constant;
    float linear;
    float quadratic;
};

const int DISCS_PCF_AMOUNT = 20;
const vec3 DISCS_PCF[DISCS_PCF_AMOUNT] = vec3[](
   vec3(1, 1, 1), vec3(1, -1, 1), vec3(-1, -1, 1),  vec3(-1, 1, 1),
   vec3(1, 1, -1),  vec3(1, -1, -1),vec3(-1, -1, -1), vec3(-1, 1, -1),
   vec3(1, 1, 0), vec3(1, -1, 0), vec3(-1, -1, 0),  vec3(-1, 1, 0),
   vec3(1, 0, 1), vec3(-1, 0, 1), vec3(1, 0, -1),   vec3(-1, 0, -1),
   vec3(0, 1, 1), vec3(0, -1, 1), vec3(0, -1, -1),  vec3(0, 1, -1)
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
    light.ambient = vec3(0.27);
    light.diffuse = vec3(0.55);
    light.specular = vec3(0.55);
    light.constant = 1.0;
    light.linear = 0.01;
    light.quadratic = 0.01;

    vec3 norm = normalize(normal);
    vec3 viewDir = normalize(viewPos - fragPos);
    float shadowVal = shadowCalculation(light);
    vec3 result = calcPointLight(light, norm, viewDir, shadowVal);
    fragColor = vec4(result, 1.0);
}

float shadowCalculation(PointLight light)
{
    const float bias = 0.12;

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
    vec3 fragToLightDir = light.position - fragPos;
    float distances = length(fragToLightDir);
    fragToLightDir = normalize(fragToLightDir);
    float weakening = 1.0 / (light.constant + light.linear * distances + light.quadratic * pow(distances, 2));

    float diff = max(dot(fragToLightDir, normal), 0.0);
    vec3 halfwayDir = normalize(fragToLightDir + viewDir);
    float specAngle = max(dot(halfwayDir, normal), 0.0);
    float spec = pow(specAngle, material.shininess);

    vec3 ambient = light.ambient * material.ambient * weakening;
    vec3 diffuse = light.diffuse * diff * weakening;
    vec3 specular = light.specular * spec * weakening;
    return (ambient + (1.0 - shadow) * (diffuse + specular)) * (material.diffuse + material.specular);
}