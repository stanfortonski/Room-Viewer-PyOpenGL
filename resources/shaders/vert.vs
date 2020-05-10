#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;

out vec3 normal;
out vec3 fragPos;

uniform mat4 viewProject;
uniform mat4 model;

void main()
{
    fragPos = vec3(model * vec4(aPos, 1.0));
    normal = aNormal * -1;
    gl_Position = viewProject * vec4(fragPos, 1.0);
}