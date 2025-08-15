# 配置文件目录说明

## 📁 目录结构

```
config/
├── README.md                    # 本说明文档
├── yaml/                       # Docker Compose配置文件
│   ├── docker-compose3.yaml    # 多浏览器Selenium Grid配置
│   └── docker-compose.jenkins_agent.yaml  # Jenkins Agent配置
├── docker/                     # Docker镜像构建文件
│   ├── Dockerfile.jenkins      # Jenkins Master镜像
│   └── Dockerfile.jenkins_agent # Jenkins Agent镜像
└── scripts/                    # 启动和管理脚本
    ├── start_jenkins_agent.sh  # Jenkins Agent启动脚本
    └── jenkins_shell.sh        # Jenkins Shell脚本
```

## 🚀 使用方法

### 启动多浏览器Selenium Grid
```bash
cd config/yaml
docker-compose -f docker-compose3.yaml up -d
```

### 启动Jenkins Agent
```bash
cd config/scripts
./start_jenkins_agent.sh
```

### 构建Jenkins Agent镜像
```bash
cd config/docker
docker build -f Dockerfile.jenkins_agent -t jenkins-agent:latest .
```

## 📋 配置说明

### Selenium Grid配置
- **端口映射**:
  - Chrome: 4444, 7900, 5900
  - Firefox: 4445, 7901, 5901
  - Edge: 4446, 7902, 5902
  - Hub: 4447, 4448

### Jenkins配置
- **Jenkins Master**: 端口8080, 50000
- **Jenkins Agent**: 自动连接到Master
- **工作目录**: 挂载到宿主机

## 🔧 维护说明

- 所有配置文件统一放在 `config/` 目录下
- 修改配置后需要重启相应的服务
- 脚本文件已设置执行权限，可直接运行
