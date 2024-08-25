# -----------------------------------------------------------------------------------------------------------------------------
# 基本信息设置
$url = "https://shgy.buaa.edu.cn/ics/rest/wxdev/getlvalue" # 根据宿舍选择查询链接，默认为西区中湾物业
$student_id = "xxxxxxxxxxxx" # 学号
$receiver_email = "email1@qq.com, email2@buaa.edu.cn" # 收件人邮箱，支持多人，不同邮箱使用逗号分隔
$sender_email = "xxxxxx" # 用于发送通知消息的邮箱，自己选择
$password = "xxxxxxxxxxxxxxx" # 是邮箱stmp的授权码，不是自己设置的登录密码
$smtp_server = "smtp.xx.com" # smtp服务器
$smtp_port = 587 # stmp端口，默认使用587端口，163邮箱需要把端口改为465
$threshold = 100 # 发送邮件的阈值，根据自己宿舍电量使用情况设置
#-----------------------------------------------------------------------------------------------------------------------------

$headers = @{
    "Content-Type" = "application/json; charset=UTF-8"
}
$json_data = @{
    "stucode" = $student_id
    "type"    = 1
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $json_data -ContentType "application/json"
$provalue = $response.data.provalue
$balance = [int]$provalue.Substring(0, $provalue.Length - 3)

$message = New-Object system.net.mail.mailmessage
$message.from = $sender_email
$message.To.add($receiver_email)
$message.Subject = "Warning"
$message.Body = "The available power is insufficient. Remaining power: " + $balance + "kWh"

$smtp = New-Object Net.Mail.SmtpClient($smtp_server, $smtp_port)
$smtp.EnableSsl = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential($sender_email, $password)

if ($balance -lt $threshold) {
    $smtp.Send($message)
}