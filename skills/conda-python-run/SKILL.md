---
name: conda-python-run
description: Run Python commands correctly on this Windows project by first detecting whether a conda virtual environment is used and activating it. Use BEFORE running ANY python/pip command (python, pip, pytest, uvicorn, python -m, jupyter, running a .py script, etc). Reads the project's remembered env from .proj_env, or asks the user which conda env to use and remembers the choice. Ensures commands run inside the right conda env instead of the system Python.
---

# 在 conda 环境中执行 Python 命令

在本项目（Windows 平台）执行任何 Python 相关命令前，必须先确认并激活正确的 conda 虚拟环境，避免误用系统 Python。

## 关键前提（本环境特性）

- 当前是 **Windows** 平台，Bash 工具底层走 Git Bash / MSYS2，`conda activate` 在其中会报 `Run 'conda init' before 'conda activate'`。
- **每条 Bash 命令都是独立的新 shell**，上一条命令里的 `conda activate` 不会保留到下一条。因此激活和后续命令**必须写在同一条命令里**。
- 用 Windows 原生命令行执行时，必须写 `cmd //c "..."`（双斜杠），否则 MSYS 会把 `/c` 当成路径。

## 决策流程（每次执行 Python 命令前）

```
读取项目根目录的 .proj_env
├─ 文件存在
│   ├─ 内容为环境名 → 步骤 B 激活并执行
│   └─ 内容为 __none__ → 不使用虚拟环境，直接执行 python 命令
└─ 文件不存在 → 步骤 A 询问用户 → 写入 .proj_env → 步骤 B 执行
```

### 步骤 A：不知道项目是否用虚拟环境时，询问用户

1. 先列出 conda 已安装的环境：
   ```bash
   cmd //c "conda env list"
   ```
2. 用 **AskUserQuestion** 工具以单选方式询问用户，选项为「每个 conda 环境」外加一个「不启用环境」：
   - 选项1：环境A
   - 选项2：环境B
   - ...
   - 选项N：不启用环境（代表不使用虚拟环境）

### 步骤 B：记忆用户选择到 `.proj_env`

用户选择后，在**项目根目录**写入记忆文件 `.proj_env`，保存本项目使用的环境：

- 选择了某个环境（如 `skl`）→ 文件内容写该环境名：
  ```bash
  cmd //c "echo skl> .proj_env"
  ```
- 选择「不启用环境」→ 文件内容写 `__none__`：
  ```bash
  cmd //c "echo __none__> .proj_env"
  ```

> 建议将 `.proj_env` 加入 `.gitignore`（属个人本地环境配置）。
> 若用户后续想切换环境，删除 `.proj_env` 或直接修改其内容即可，下次会重新询问。

### 步骤 C：读取记忆并执行 Python 命令

每次执行前先读取 `.proj_env` 判断：

```bash
# 读取记忆的环境名（去除空白）
cat .proj_env 2>/dev/null
```

- 若为具体环境名 `<env>`，激活并执行（合并成一条）：
  ```bash
  cmd //c "conda activate <env> && <后续命令>"
  ```
- 若为 `__none__`，不激活，直接执行：
  ```bash
  cmd //c "<后续命令>"
  ```
- 若文件不存在，回到 **步骤 A** 询问用户。

## 执行示例（以环境名 `skl` 为例）

```bash
# 确认激活成功
cmd //c "conda activate skl && python --version && where python"

# 运行脚本 / 模块 / 测试
cmd //c "conda activate skl && python your_script.py"
cmd //c "conda activate skl && python -m pytest"

# 包管理 / 启动服务
cmd //c "conda activate skl && pip list"
cmd //c "conda activate skl && uvicorn app.main:app --reload"
```

## 检查清单

- [ ] 执行前已读取 `.proj_env`
- [ ] 文件不存在时，列出 `conda env list` 并用 AskUserQuestion 单选询问（含「不启用环境」选项）
- [ ] 用户选择后已写入 `.proj_env`（环境名 或 `__none__`）
- [ ] 激活与执行命令写在**同一条** `cmd //c "..."` 里，且用 `//c`（双斜杠）
- [ ] `.proj_env` 为 `__none__` 时跳过激活直接执行
