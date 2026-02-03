---
name: java-runner
description: 执行 Java 类的 main 方法或 JUnit 测试方法，适用于 Maven 多模块项目中的测试类或工具类。
---
# Run Java Main Method & JUnit Tests

## 描述

执行 Java 类的 main 方法或 JUnit 测试方法，适用于 Maven 多模块项目中的测试类或工具类。

## 使用场景

- 执行测试类的 main 方法进行快速验证
- 运行 JUnit 测试类或特定测试方法
- 运行工具类进行数据处理或测试
- 在多模块 Maven 项目中执行特定模块的 Java 类或测试

## 执行步骤

### 0. 配置检查与初始化

在执行任何 Maven 或 Java 命令前，必须先确保配置已正确设置：

#### 0.1 检查配置是否存在

使用 `config_manager.py` 检查配置：

```bash
python scripts/config_manager.py show
```

#### 0.2 首次配置或配置缺失

如果配置文件不存在（`~/.skills/java-skill.conf`），需要先进行配置：

```bash
python scripts/config_manager.py
```

系统会提示输入以下配置信息：
- **Java Home 路径**：JDK 安装目录（例如：`C:/Program Files/Java/jdk-17`）
- **Maven Home 路径**：Maven 安装目录（例如：`C:/apache-maven-3.9.0`）
- **Maven settings.xml 路径**（可选）：自定义 Maven 配置文件路径
- **默认 JVM 参数**（可选）：如 `-Xmx2g -Xms512m`
- **默认 Maven 参数**（可选）：如 `-T 4`

#### 0.3 重置配置

如果需要修改配置：

```bash
python scripts/config_manager.py reset
```

#### 0.4 获取配置值

在执行命令前，使用 `config_manager.load_config()` 获取配置：

```python
from config_manager import load_config

config = load_config()
java_home = config.get('java_home')
maven_home = config.get('maven_home')
maven_settings = config.get('maven_settings', '')
```

**重要说明**：
- 所有 Maven 命令必须使用配置中的 `maven_home` 路径
- 所有 Java 命令必须使用配置中的 `java_home` 路径
- 如果配置了 `maven_settings`，Maven 命令需要添加 `-s` 参数指定配置文件

## 方式一：执行 Main 方法

### 1. 定位目标类

首先找到要执行的 Java 类文件位置：

```bash
# 使用 Glob 工具查找类文件
pattern: **/ClassName.java
```

### 2. 确定项目结构

检查项目是否为多模块项目：

```bash
find "项目根目录" -maxdepth 2 -name "pom.xml" -type f
```

### 3. 安装本地依赖（多模块项目）

如果是多模块项目，需要先安装本地依赖到 Maven 仓库：

```bash
cd "模块根目录"
# 使用配置中的 Maven 路径执行命令
{maven_home}/bin/mvn install -DskipTests
# 如果配置了 maven_settings，添加 -s 参数
{maven_home}/bin/mvn install -DskipTests -s {maven_settings}
```

**说明**：
- `{maven_home}` 需要替换为配置中的 Maven Home 路径
- `{maven_settings}` 需要替换为配置中的 Maven settings.xml 路径（如果配置了）
- `-DskipTests` 跳过测试，加快构建速度
- 这一步确保模块间的依赖能够正确解析

### 4. 执行 Main 方法

使用 Maven exec 插件执行目标类：

```bash
cd "包含目标类的子模块目录"
# 使用配置中的 Maven 路径执行命令
{maven_home}/bin/mvn exec:java -Dexec.mainClass="完整类名"
# 如果配置了 maven_settings，添加 -s 参数
{maven_home}/bin/mvn exec:java -Dexec.mainClass="完整类名" -s {maven_settings}
```

**参数说明**：
- `{maven_home}` 需要替换为配置中的 Maven Home 路径
- `{maven_settings}` 需要替换为配置中的 Maven settings.xml 路径（如果配置了）
- `exec:java` - Maven exec 插件的 goal
- `-Dexec.mainClass` - 指定要执行的类的完全限定名（包名.类名）

### 5. 可选参数

如果需要传递参数或 JVM 选项：

```bash
# 传递程序参数
{maven_home}/bin/mvn exec:java -Dexec.mainClass="类名" -Dexec.args="arg1 arg2"

# 设置 JVM 参数
{maven_home}/bin/mvn exec:java -Dexec.mainClass="类名" -Dexec.args="-Xmx2g -Denv=dev"

# 如果配置了 maven_settings
{maven_home}/bin/mvn exec:java -Dexec.mainClass="类名" -Dexec.args="arg1 arg2" -s {maven_settings}
```

## 方式二：执行 JUnit 测试

### 1. 定位测试类

查找测试类文件（通常在 src/test/java 目录下）：

```bash
# 使用 Glob 工具查找测试类
pattern: **/TestClassName.java
# 或查找所有测试类
pattern: **/*Test.java
```

### 2. 编译测试代码

确保测试代码已编译：

```bash
cd "模块目录"
# 使用配置中的 Maven 路径执行命令
{maven_home}/bin/mvn test-compile
# 如果配置了 maven_settings
{maven_home}/bin/mvn test-compile -s {maven_settings}
```

### 3. 运行测试

#### 3.1 运行所有测试

```bash
{maven_home}/bin/mvn test
# 如果配置了 maven_settings
{maven_home}/bin/mvn test -s {maven_settings}
```

#### 3.2 运行特定测试类

```bash
{maven_home}/bin/mvn test -Dtest=TestClassName
# 如果配置了 maven_settings
{maven_home}/bin/mvn test -Dtest=TestClassName -s {maven_settings}
```

**示例**：
```bash
# 运行 UserServiceTest 类的所有测试方法
{maven_home}/bin/mvn test -Dtest=UserServiceTest

# 支持通配符
{maven_home}/bin/mvn test -Dtest=*ServiceTest
{maven_home}/bin/mvn test -Dtest=User*Test
```

#### 3.3 运行特定测试方法

```bash
# 运行单个测试方法
{maven_home}/bin/mvn test -Dtest=TestClassName#testMethodName

# 运行多个测试方法
{maven_home}/bin/mvn test -Dtest=TestClassName#testMethod1+testMethod2
```

**示例**：
```bash
# 运行 UserServiceTest 类的 testCreateUser 方法
{maven_home}/bin/mvn test -Dtest=UserServiceTest#testCreateUser

# 运行多个测试方法
{maven_home}/bin/mvn test -Dtest=UserServiceTest#testCreateUser+testUpdateUser

# 使用通配符匹配测试方法
{maven_home}/bin/mvn test -Dtest=UserServiceTest#test*User
```

#### 3.4 运行多个测试类

```bash
# 使用逗号分隔多个测试类
{maven_home}/bin/mvn test -Dtest=TestClass1,TestClass2

# 结合通配符
{maven_home}/bin/mvn test -Dtest=*ServiceTest,*ControllerTest
```

### 4. 测试输出控制

```bash
# 显示详细测试输出
{maven_home}/bin/mvn test -Dtest=TestClassName -X

# 跳过测试失败继续执行
{maven_home}/bin/mvn test -Dmaven.test.failure.ignore=true

# 并行运行测试（加快速度）
{maven_home}/bin/mvn test -T 4

# 只运行失败的测试
{maven_home}/bin/mvn test -Dsurefire.rerunFailingTestsCount=2
```

### 5. JUnit 5 特定功能

```bash
# 按标签运行测试（需要 @Tag 注解）
{maven_home}/bin/mvn test -Dgroups="integration"

# 排除特定标签
{maven_home}/bin/mvn test -DexcludedGroups="slow"

# 组合使用
{maven_home}/bin/mvn test -Dgroups="integration" -DexcludedGroups="slow"
```

## 示例

### 示例 1: 执行 MyExcelUtilsTest 的 Main 方法

```bash
# 0. 检查配置
python scripts/config_manager.py show

# 1. 查找类文件
Glob: **/MyExcelUtilsTest.java
# 结果: D:\workspace\...\xs-servarea-provider\src\main\java\cn\xs\servarea\test\MyExcelUtilsTest.java

# 2. 安装依赖（假设 maven_home 为 C:/apache-maven-3.9.0）
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-servarea"
C:/apache-maven-3.9.0/bin/mvn install -DskipTests

# 3. 执行 main 方法
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-servarea\xs-servarea-provider"
C:/apache-maven-3.9.0/bin/mvn exec:java -Dexec.mainClass="cn.xs.servarea.test.MyExcelUtilsTest"
```

### 示例 2: 运行单个 JUnit 测试类

```bash
# 0. 检查配置
python scripts/config_manager.py show

# 1. 查找测试类
Glob: **/UserServiceTest.java
# 结果: D:\workspace\...\service\src\test\java\cn\xs\service\UserServiceTest.java

# 2. 编译测试代码（假设 maven_home 为 C:/apache-maven-3.9.0）
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-service"
C:/apache-maven-3.9.0/bin/mvn test-compile

# 3. 运行测试类
C:/apache-maven-3.9.0/bin/mvn test -Dtest=UserServiceTest
```

### 示例 3: 运行特定测试方法

```bash
# 运行 UserServiceTest 的 testCreateUser 方法（假设 maven_home 为 C:/apache-maven-3.9.0）
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-service"
C:/apache-maven-3.9.0/bin/mvn test -Dtest=UserServiceTest#testCreateUser

# 运行多个测试方法
C:/apache-maven-3.9.0/bin/mvn test -Dtest=UserServiceTest#testCreateUser+testUpdateUser+testDeleteUser
```

### 示例 4: 运行所有 Service 层测试

```bash
# 使用通配符运行所有 Service 测试（假设 maven_home 为 C:/apache-maven-3.9.0）
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-service"
C:/apache-maven-3.9.0/bin/mvn test -Dtest=*ServiceTest
```

## 常见问题

### 问题 1: Could not resolve dependencies

**原因**：多模块项目的模块间依赖未安装到本地仓库

**解决**：在父模块或包含所有依赖的模块执行 `mvn install -DskipTests`

### 问题 2: ClassNotFoundException 或 NoClassDefFoundError

**原因**：类路径不完整，缺少依赖

**解决**：
1. 确保已执行 `mvn compile` 编译项目
2. 使用 `mvn exec:java` 而不是直接用 `java` 命令，因为 exec 插件会自动处理类路径

### 问题 3: 找不到 pom.xml

**原因**：当前目录不是 Maven 项目根目录

**解决**：使用 `cd` 切换到包含 pom.xml 的目录

### 问题 4: No tests were executed

**原因**：
- 测试类名或方法名拼写错误
- 测试类未编译
- 测试类不在标准的 src/test/java 目录下

**解决**：
1. 检查测试类名和方法名是否正确
2. 执行 `mvn test-compile` 编译测试代码
3. 使用 `-X` 参数查看详细日志：`mvn test -Dtest=TestClass -X`

### 问题 5: 测试失败但想继续执行

**原因**：默认情况下，测试失败会中断构建

**解决**：使用 `-Dmaven.test.failure.ignore=true` 参数

## 注意事项

1. **配置优先**：在执行任何命令前，必须先确保配置已正确设置（使用 `config_manager.py`）
2. **使用配置路径**：所有 Maven 和 Java 命令必须使用配置文件中指定的路径
3. **工作目录**：确保在正确的模块目录下执行命令
4. **类名格式**：
   - Main 方法：必须使用完全限定名（包名.类名），如 `cn.xs.servarea.test.MyExcelUtilsTest`
   - 测试类：只需要类名，如 `UserServiceTest`，Maven 会自动查找
5. **依赖顺序**：在多模块项目中，先安装依赖再执行
6. **编译状态**：如果代码有修改，先执行编译命令重新编译
7. **测试命名规范**：
   - JUnit 测试类通常以 `Test` 结尾或以 `Test` 开头
   - 测试方法通常以 `test` 开头（JUnit 4）或使用 `@Test` 注解（JUnit 5）
8. **Maven Settings**：如果配置了自定义的 `maven_settings`，记得在命令中添加 `-s {maven_settings}` 参数

## 相关命令

**注意**：以下所有命令中的 `{maven_home}` 需要替换为配置中的 Maven Home 路径，`{maven_settings}` 需要替换为配置中的 Maven settings.xml 路径（如果配置了）。

```bash
# 查看当前配置
python scripts/config_manager.py show

# 重置配置
python scripts/config_manager.py reset

# 编译项目
{maven_home}/bin/mvn compile

# 编译测试代码
{maven_home}/bin/mvn test-compile

# 编译并安装到本地仓库
{maven_home}/bin/mvn install

# 只编译不运行测试
{maven_home}/bin/mvn compile -DskipTests

# 清理并重新编译
{maven_home}/bin/mvn clean compile

# 运行所有测试
{maven_home}/bin/mvn test

# 运行特定测试类
{maven_home}/bin/mvn test -Dtest=TestClassName

# 运行特定测试方法
{maven_home}/bin/mvn test -Dtest=TestClassName#testMethod

# 跳过测试
{maven_home}/bin/mvn install -DskipTests

# 查看项目依赖树
{maven_home}/bin/mvn dependency:tree

# 查看有效的 POM 配置
{maven_home}/bin/mvn help:effective-pom

# 查看测试报告
# 报告位置: target/surefire-reports/
ls target/surefire-reports/

# 如果配置了 maven_settings，在命令后添加 -s 参数
{maven_home}/bin/mvn compile -s {maven_settings}
{maven_home}/bin/mvn test -Dtest=TestClassName -s {maven_settings}
```
