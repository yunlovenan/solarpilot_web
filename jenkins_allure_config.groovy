// Jenkins Allure配置脚本
// 在Jenkins Script Console中运行此脚本来配置Allure

import jenkins.model.*
import hudson.model.*
import ru.yandex.qameta.allure.jenkins.AllureReportPublisher
import ru.yandex.qatools.allure.jenkins.AllureCommandlineInstallation

// 获取Jenkins实例
def jenkins = Jenkins.instance

// 配置Allure Commandline工具
def allureInstallation = new AllureCommandlineInstallation(
    "Allure",  // 名称
    "/usr/local/bin/allure",  // 安装路径
    []  // 属性
)

// 获取全局工具配置
def toolConfig = jenkins.getDescriptor("hudson.plugins.sshslaves.SSHLauncher")
if (toolConfig != null) {
    // 添加Allure安装
    def installations = toolConfig.getInstallations()
    def newInstallations = new AllureCommandlineInstallation[installations.length + 1]
    System.arraycopy(installations, 0, newInstallations, 0, installations.length)
    newInstallations[installations.length] = allureInstallation
    toolConfig.setInstallations(newInstallations)
    toolConfig.save()
    println "✅ Allure Commandline工具配置成功"
} else {
    println "❌ 无法获取工具配置"
}

// 配置项目级别的Allure报告
def job = jenkins.getItem("solar_web")
if (job != null) {
    def config = job.getConfigFile()
    if (config != null) {
        def xml = config.asString()
        
        // 添加Allure Report Publisher
        def allurePublisher = new AllureReportPublisher(
            "ALLURE-RESULTS",  // 结果路径
            "allure-report",   // 报告路径
            false,             // 包含属性
            "",                // JDK
            [],                // 属性
            "ALWAYS"           // 报告构建策略
        )
        
        // 更新项目配置
        job.updateByXml(new XmlSlurper().parseText(xml))
        println "✅ 项目Allure配置更新成功"
    } else {
        println "❌ 无法获取项目配置"
    }
} else {
    println "❌ 项目solar_web不存在"
}

println "🎉 Allure配置完成！" 