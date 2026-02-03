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
mvn install -DskipTests
```

**说明**：
- `-DskipTests` 跳过测试，加快构建速度
- 这一步确保模块间的依赖能够正确解析

### 4. 执行 Main 方法

使用 Maven exec 插件执行目标类：

```bash
cd "包含目标类的子模块目录"
mvn exec:java -Dexec.mainClass="完整类名"
```

**参数说明**：
- `exec:java` - Maven exec 插件的 goal
- `-Dexec.mainClass` - 指定要执行的类的完全限定名（包名.类名）

### 5. 可选参数

如果需要传递参数或 JVM 选项：

```bash
# 传递程序参数
mvn exec:java -Dexec.mainClass="类名" -Dexec.args="arg1 arg2"

# 设置 JVM 参数
mvn exec:java -Dexec.mainClass="类名" -Dexec.args="-Xmx2g -Denv=dev"
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
mvn test-compile
```

### 3. 运行测试

#### 3.1 运行所有测试

```bash
mvn test
```

#### 3.2 运行特定测试类

```bash
mvn test -Dtest=TestClassName
```

**示例**：
```bash
# 运行 UserServiceTest 类的所有测试方法
mvn test -Dtest=UserServiceTest

# 支持通配符
mvn test -Dtest=*ServiceTest
mvn test -Dtest=User*Test
```

#### 3.3 运行特定测试方法

```bash
# 运行单个测试方法
mvn test -Dtest=TestClassName#testMethodName

# 运行多个测试方法
mvn test -Dtest=TestClassName#testMethod1+testMethod2
```

**示例**：
```bash
# 运行 UserServiceTest 类的 testCreateUser 方法
mvn test -Dtest=UserServiceTest#testCreateUser

# 运行多个测试方法
mvn test -Dtest=UserServiceTest#testCreateUser+testUpdateUser

# 使用通配符匹配测试方法
mvn test -Dtest=UserServiceTest#test*User
```

#### 3.4 运行多个测试类

```bash
# 使用逗号分隔多个测试类
mvn test -Dtest=TestClass1,TestClass2

# 结合通配符
mvn test -Dtest=*ServiceTest,*ControllerTest
```

### 4. 测试输出控制

```bash
# 显示详细测试输出
mvn test -Dtest=TestClassName -X

# 跳过测试失败继续执行
mvn test -Dmaven.test.failure.ignore=true

# 并行运行测试（加快速度）
mvn test -T 4

# 只运行失败的测试
mvn test -Dsurefire.rerunFailingTestsCount=2
```

### 5. JUnit 5 特定功能

```bash
# 按标签运行测试（需要 @Tag 注解）
mvn test -Dgroups="integration"

# 排除特定标签
mvn test -DexcludedGroups="slow"

# 组合使用
mvn test -Dgroups="integration" -DexcludedGroups="slow"
```

## 示例

### 示例 1: 执行 MyExcelUtilsTest 的 Main 方法

```bash
# 1. 查找类文件
Glob: **/MyExcelUtilsTest.java
# 结果: D:\workspace\...\xs-servarea-provider\src\main\java\cn\xs\servarea\test\MyExcelUtilsTest.java

# 2. 安装依赖
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-servarea"
mvn install -DskipTests

# 3. 执行 main 方法
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-servarea\xs-servarea-provider"
mvn exec:java -Dexec.mainClass="cn.xs.servarea.test.MyExcelUtilsTest"
```

### 示例 2: 运行单个 JUnit 测试类

```bash
# 1. 查找测试类
Glob: **/UserServiceTest.java
# 结果: D:\workspace\...\service\src\test\java\cn\xs\service\UserServiceTest.java

# 2. 编译测试代码
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-service"
mvn test-compile

# 3. 运行测试类
mvn test -Dtest=UserServiceTest
```

### 示例 3: 运行特定测试方法

```bash
# 运行 UserServiceTest 的 testCreateUser 方法
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-service"
mvn test -Dtest=UserServiceTest#testCreateUser

# 运行多个测试方法
mvn test -Dtest=UserServiceTest#testCreateUser+testUpdateUser+testDeleteUser
```

### 示例 4: 运行所有 Service 层测试

```bash
# 使用通配符运行所有 Service 测试
cd "D:\workspace\com.xiaoshi\gitlab\backendservice\motsa\xs-motsa-service"
mvn test -Dtest=*ServiceTest
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

1. **工作目录**：确保在正确的模块目录下执行命令
2. **类名格式**：
   - Main 方法：必须使用完全限定名（包名.类名），如 `cn.xs.servarea.test.MyExcelUtilsTest`
   - 测试类：只需要类名，如 `UserServiceTest`，Maven 会自动查找
3. **依赖顺序**：在多模块项目中，先安装依赖再执行
4. **编译状态**：如果代码有修改，先执行 `mvn compile` 或 `mvn test-compile` 重新编译
5. **测试命名规范**：
   - JUnit 测试类通常以 `Test` 结尾或以 `Test` 开头
   - 测试方法通常以 `test` 开头（JUnit 4）或使用 `@Test` 注解（JUnit 5）

## 相关命令

```bash
# 编译项目
mvn compile

# 编译测试代码
mvn test-compile

# 编译并安装到本地仓库
mvn install

# 只编译不运行测试
mvn compile -DskipTests

# 清理并重新编译
mvn clean compile

# 运行所有测试
mvn test

# 运行特定测试类
mvn test -Dtest=TestClassName

# 运行特定测试方法
mvn test -Dtest=TestClassName#testMethod

# 跳过测试
mvn install -DskipTests

# 查看项目依赖树
mvn dependency:tree

# 查看有效的 POM 配置
mvn help:effective-pom

# 查看测试报告
# 报告位置: target/surefire-reports/
ls target/surefire-reports/
```
