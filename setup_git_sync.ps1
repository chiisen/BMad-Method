# setup_git_sync.ps1
# 依據 docs/git同步備份branch.md 建立的同步腳本

$RepoName = "BMad-Method"

$BackupUrl = "git@github.com:edwin45168899/$RepoName.git"
$MainUrl = "git@github.com-chiisen:chiisen/$RepoName.git"
$MainUrl1 = "git@github.com-edwiin1688:edwiin1688/$RepoName.git"
$MainUrl2 = "git@github.com-NathanEvans1221:NathanEvans1221/$RepoName.git"

Write-Output "正在設定 Git 遠端同步 (Repo: $RepoName)..."
Write-Output "備份遠端: $BackupUrl"
Write-Output "主要遠端: $MainUrl"
Write-Output "主要遠端1: $MainUrl1"
Write-Output "主要遠端2: $MainUrl2"

# 1. 徹底清除所有已堆疊的 push 位址 (防止重複執行導致堆疊)
git config --unset-all remote.origin.pushurl 2>$null

# 2. 依序重新新增所有的 push 位址
git remote set-url --add --push origin $MainUrl
git remote set-url --add --push origin $BackupUrl
git remote set-url --add --push origin $MainUrl1
git remote set-url --add --push origin $MainUrl2

Write-Output "設定完成。目前的 remote 設定如下："
git remote -v

