# JUnit 测试运行模式

## JUnit 4 和 JUnit 5

### 运行单个测试类
```bash
# JUnit 4 和 JUnit 5 都支持
mvn test -Dtest=MyTestClass
```

### 运行单个测试方法
```bash
# JUnit 4
mvn test -Dtest=MyTestClass#testMethod

# JUnit 5
mvn test -Dtest=MyTestClass#testMethod
```

### 运行多个测试方法
```bash
# JUnit 4
mvn test -Dtest=MyTestClass#testMethod1+testMethod2

# JUnit 5
mvn test -Dtest=MyTestClass#testMethod1,testMethod2
```

## 测试过滤

### 使用通配符
```bash
# 运行所有以 Test 结尾的类
mvn test -Dtest=*Test

# 运行所有以 Service 开头的测试类
mvn test -Dtest=Service*

# 运行特定包下的所有测试
mvn test -Dtest=com.example.service.*Test
```

### 运行多个测试类
```bash
mvn test -Dtest=TestClass1,TestClass2,TestClass3
```

### 排除测试
```bash
# 在 pom.xml 中配置
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <excludes>
            <exclude>**/*IntegrationTest.java</exclude>
        </excludes>
    </configuration>
</plugin>
```

## 测试分组

### JUnit 5 标签（Tags）
```java
@Tag("fast")
@Test
void fastTest() {
    // 快速测试
}

@Tag("slow")
@Test
void slowTest() {
    // 慢速测试
}
```

运行特定标签的测试：
```bash
mvn test -Dgroups=fast
mvn test -Dgroups="fast | slow"
mvn test -Dgroups="fast & !slow"
```

### JUnit 4 分类（Categories）
```java
public interface FastTests {}
public interface SlowTests {}

@Category(FastTests.class)
@Test
public void fastTest() {
    // 快速测试
}
```

运行特定分类的测试：
```bash
mvn test -Dgroups=com.example.FastTests
```

## 测试报告

### 生成测试报告
```bash
mvn surefire-report:report
```

### 查看测试结果
测试结果位于：`target/surefire-reports/`

## 常见问题

### 测试失败后继续构建
```bash
mvn test -Dmaven.test.failure.ignore=true
```

### 重新运行失败的测试
```bash
mvn surefire:test -Dsurefire.rerunFailingTestsCount=2
```

### 并行运行测试
```bash
mvn test -Dparallel=methods -DthreadCount=4
```

### 设置测试超时
```bash
mvn test -Dsurefire.timeout=300
```

## TestNG 支持

### 运行 TestNG 测试
```bash
mvn test -Dtest=MyTestNGClass
```

### 使用 TestNG XML 配置
```bash
mvn test -DsuiteXmlFile=testng.xml
```

### 运行特定组
```bash
mvn test -Dgroups=smoke,regression
```
