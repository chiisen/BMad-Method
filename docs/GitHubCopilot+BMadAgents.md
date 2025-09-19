已經完成 BMad-Method 的安裝與設定，現在可以正式啟用 GitHub Copilot 來進行專案開發了。  
以下是完整的操作流程，結合 BMad 的 agent 模型與 Copilot 的 IDE 整合：  

---

## 🚀 啟用 GitHub Copilot + BMad Agents 專案開發流程

### 1. ✅ 安裝時選擇 Copilot 模式
如果你是透過 `npx bmad-method install` 安裝的，請確認你有選擇 `GitHub Copilot` 作為 IDE。這會自動執行以下設定：

- 建立 `.bmad-core/` 資料夾，內含所有 agent 的規則檔案
- 建立 `.vscode/settings.json`，啟用 Copilot 的 agent 模式
- 在 `.github/` 資料夾下建立 `chatmodes` 設定檔，定義各 agent 的角色

---

### 2. 🧠 開啟 Copilot Chat 面板

在 VS Code 中使用快捷鍵開啟 Copilot Chat：

- macOS：`⌃⌘I`
- Windows / Linux：`Ctrl + Alt + I`

你會看到一個聊天面板，左側可以選擇 agent，例如：

| Agent 名稱       | 角色說明                     |
|------------------|------------------------------|
| `@workspace > dev` | 專案開發工程師（Dev）         |
| `@workspace > qa`  | 測試與品質保證（QA）          |
| `@workspace > ux`  | 使用者體驗設計師（UX Expert） |
| `@workspace > bmad-master` | 任務總管，負責協調與執行 |

---

### 3. 🧪 使用 agent 指令進行開發

在 Copilot Chat 中選擇 agent 後，你可以輸入指令，例如：

- `*help`：查看該 agent 支援的所有指令
- `*create story`：建立開發任務故事（Story）
- `*run task`：執行某個任務（例如 `npm run build`）
- `*autoFix`：自動偵測並修復錯誤

這些指令會根據你選的 agent 自動執行對應的任務，並根據 BMad 的上下文（PRD、架構、任務流程）產生具備完整背景的程式碼。

---

### 4. ⚙️ VS Code 設定建議

你可以在 `.vscode/settings.json` 中調整以下參數：

```json
{
  "github.copilot.chat.agent.runTasks": true,
  "github.copilot.chat.agent.autoFix": true,
  "chat.agent.maxRequests": 15,
  "chat.tools.autoApprove": false
}
```

這些設定會讓 Copilot 的 agent 模式更順暢，並確保你可以安全地執行任務與修正錯誤。

---

### 5. 📁 提供額外上下文（選用）

你也可以建立 `.github/copilot-instructions.md`，放入專案的額外說明，例如：

- 專案架構簡介
- API 規格
- 安全性注意事項（如 HSTS、proxy 設定）

這樣 Copilot agent 在生成程式碼時會更有上下文，產出更精準。

---

如果你想，我可以幫你設定一個 `dev agent` 的開發任務流程，或模擬一次 `*create story` 的使用情境。你想針對哪個模組開始開發？前端、API 還是 proxy？