# Maven 常用命令参考

## 编译和构建

### 编译项目
```bash
mvn compile
```

### 编译测试代码
```bash
mvn test-compile
```

### 打包项目
```bash
mvn package
```

### 清理构建产物
```bash
mvn clean
```

### 清理并打包
```bash
mvn clean package
```

## 测试相关

### 运行所有测试
```bash
mvn test
```

### 运行指定测试类
```bash
mvn test -Dtest=MyTestClass
```

### 运行指定测试方法
```bash
mvn test -Dtest=MyTestClass#testMethod
```

### 运行多个测试类
```bash
mvn test -Dtest=MyTestClass1,MyTestClass2
```

### 使用通配符运行测试
```bash
mvn test -Dtest=*ServiceTest
```

### 跳过测试
```bash
mvn package -DskipTests
```

### 跳过测试编译和执行
```bash
mvn package -Dmaven.test.skip=true
```

## 依赖管理

### 查看依赖树
```bash
mvn dependency:tree
```

### 获取 classpath
```bash
mvn dependency:build-classpath
```

### 下载依赖源码
```bash
mvn dependency:sources
```

### 分析依赖
```bash
mvn dependency:analyze
```

## 使用自定义 settings.xml

### 指定 settings.xml 文件
```bash
mvn -s /path/to/settings.xml clean install
```

### 使用全局 settings.xml
默认位置：`${MAVEN_HOME}/conf/settings.xml`

### 使用用户 settings.xml
默认位置：`${user.home}/.m2/settings.xml`

## 常用参数

### 离线模式
```bash
mvn -o package
```

### 强制更新快照
```bash
mvn -U clean install
```

### 显示详细输出
```bash
mvn -X clean install
```

### 静默模式
```bash
mvn -q clean install
```

### 多线程构建
```bash
mvn -T 4 clean install
```

## 运行 Java 主类

### 使用 exec 插件运行主类
```bash
mvn exec:java -Dexec.mainClass="com.example.Main"
```

### 传递参数
```bash
mvn exec:java -Dexec.mainClass="com.example.Main" -Dexec.args="arg1 arg2"
```

### 指定 classpath
```bash
mvn exec:java -Dexec.mainClass="com.example.Main" -Dexec.classpathScope=runtime
```
