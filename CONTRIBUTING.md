# 成员提交指南

## 1. 确认任务

从 [Issues](https://github.com/wzm-Epoch/zhaogege/issues) 找到负责人发布的任务，确认作业编号、要求和截止时间。没有明确编号或要求时，先在任务下询问负责人，不自行猜测。

## 2. 准备文件

复制 [作业模板](templates/homework.md)，保存为：

```text
assignments/<作业编号>/<GitHub用户名>/README.md
```

例如，编号为 `task-001`、用户名为 `octocat` 时，路径是 `assignments/task-001/octocat/README.md`。这只是路径示例，不代表已经发布该作业。

程序、图片和报告放在同一个个人目录中。README 说明完成内容、运行或查看方式、结果及参考来源。无需运行的作业写明查看方式即可。

- 用相对路径引用同目录图片或附件，例如 `![结果](result.png)`。
- 单个文件不超过 10 MiB；大型数据、视频等使用负责人认可的外部链接，并确认他人有访问权限。
- 不提交虚拟环境、依赖安装目录、缓存和私人信息。
- 周总结使用 [周总结模板](templates/weekly-summary.md)，保存到 `ai-learning-notes/每周分享总结/YYYY-MM-DD/GitHub用户名.md`，日期取分享当天。

## 3. 网页提交（无需安装 Git）

### 没有仓库写入权限

1. 在仓库首页点击 **Fork**，创建自己的副本；已有副本先用 **Sync fork** 同步。
2. 在自己的副本点击 **Add file → Create new file**，填写完整文件路径，粘贴模板并完成内容。附件可用 **Upload files** 上传到自己的作业目录。
3. 提交文件后点击 **Contribute → Open pull request**。
4. 检查目标是 `wzm-Epoch/zhaogege` 的 `main`，来源是自己副本的分支。

### 已有仓库写入权限

1. 在仓库分支选择器中，基于最新 `main` 创建个人分支，例如 `homework/octocat-task-001`。
2. 确认当前处于个人分支，再通过 **Add file** 创建或上传文件。
3. 在 **Pull requests → New pull request** 中，选择 `base: main`、`compare: 个人分支`。

## 4. 提交与修改 PR

标题建议：`[作业] 作业编号 / GitHub用户名`；周总结使用 `[周总结] 日期 / GitHub用户名`。

填写自动出现的 PR 模板，在正文写 `Refs #任务编号` 关联任务。不要用 `Closes #任务编号`，以免个人作业合并后提前关闭全体成员的任务。

提交前在 **Files changed** 确认只包含本次作业及必要文件。等待负责人审核；收到修改意见后，继续编辑同一来源分支，PR 会自动更新，无需重复新建。合并后可删除个人分支，下次从最新 `main` 创建新分支。

如果自动检查失败，打开 PR 的 **Checks** 查看具体文件和原因；不清楚时在 PR 下说明情况。涉及他人内容或冲突时，先与负责人沟通。

## 5. 提问和资源分享

到 [新建 Issue](https://github.com/wzm-Epoch/zhaogege/issues/new/choose) 选择“学习提问”或“资源分享”。先搜索已有讨论，尽量复用同一主题；作业的专属问题可以直接在对应任务或 PR 下讨论。
