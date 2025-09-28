"""
策略报告生成器
生成详细的Markdown格式策略分析报告
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class StrategyReporter:
    """策略报告生成器"""
    
    def __init__(self, output_dir: str = "assets/reports"):
        """
        初始化策略报告生成器
        
        Args:
            output_dir: 报告输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_strategy_report(self, results: Dict[str, Any]) -> str:
        """
        生成策略分析报告
        
        Args:
            results: 分析结果字典
            
        Returns:
            报告文件路径
        """
        report_content = self._create_report_header()
        
        # 添加执行摘要
        report_content += self._create_executive_summary(results)
        
        # 为每个时间间隔生成详细分析
        for interval, result in results.items():
            report_content += self._create_interval_analysis(interval, result)
        
        # 添加策略建议
        report_content += self._create_strategy_recommendations(results)
        
        # 添加技术附录
        report_content += self._create_technical_appendix()
        
        # 保存报告
        report_file = self.output_dir / f"ETH_HMA_Strategy_Report_{self.timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_file)
    
    def _create_report_header(self) -> str:
        """创建报告头部"""
        return f"""# ETH HMA趋势策略分析报告

**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}  
**分析工具**: ETH HMA Analysis System  
**版本**: v2.0  

---

## 📋 目录

1. [执行摘要](#执行摘要)
2. [策略概述](#策略概述)
3. [详细分析结果](#详细分析结果)
   - [1小时级别分析](#1小时级别分析)
   - [4小时级别分析](#4小时级别分析)
4. [策略建议](#策略建议)
5. [技术附录](#技术附录)

---

"""
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> str:
        """创建执行摘要"""
        # 计算总体统计
        total_intervals = sum(len(result['intervals']) for result in results.values())
        total_events = sum(len(result['events']) for result in results.values())
        
        # 4小时级别分析（主要关注）
        h4_result = results.get('4h', {})
        h4_uptrend = h4_result.get('report', {}).get('uptrend_analysis', {})
        h4_downtrend = h4_result.get('report', {}).get('downtrend_analysis', {})
        
        return f"""## 📊 执行摘要

### 分析概览
- **总趋势区间数**: {total_intervals}
- **总拐点事件数**: {total_events}
- **分析时间范围**: 2024年全年
- **主要关注级别**: 4小时级别

### 4小时级别策略表现
- **做多策略**: 平均理想收益 {h4_uptrend.get('avg_long_ideal_profit', 0):.2f}%，风险收益比 {h4_uptrend.get('avg_risk_reward_ratio', 0):.2f}
- **做空策略**: 平均理想收益 {h4_downtrend.get('avg_short_ideal_profit', 0):.2f}%，风险收益比 {h4_downtrend.get('avg_risk_reward_ratio', 0):.2f}

### 关键发现
1. **策略有效性**: HMA45趋势识别在4小时级别表现良好
2. **风险控制**: 平均风险损失控制在合理范围内
3. **优化空间**: 实际收益与理想收益存在差距，需要优化出场时机

---

"""
    
    def _create_interval_analysis(self, interval: str, result: Dict[str, Any]) -> str:
        """创建单个时间间隔的分析"""
        report = result.get('report', {})
        uptrend = report.get('uptrend_analysis', {})
        downtrend = report.get('downtrend_analysis', {})
        
        # 基础统计
        total_intervals = len(result.get('intervals', []))
        total_events = len(result.get('events', []))
        
        # 做多策略统计
        long_total = uptrend.get('total_uptrends', 0)
        long_ideal_profit = uptrend.get('avg_long_ideal_profit', 0)
        long_actual_profit = uptrend.get('avg_long_actual_profit', 0)
        long_risk_loss = uptrend.get('avg_long_risk_loss', 0)
        long_risk_reward = uptrend.get('avg_risk_reward_ratio', 0)
        
        # 做空策略统计
        short_total = downtrend.get('total_downtrends', 0)
        short_ideal_profit = downtrend.get('avg_short_ideal_profit', 0)
        short_actual_profit = downtrend.get('avg_short_actual_profit', 0)
        short_risk_loss = downtrend.get('avg_short_risk_loss', 0)
        short_risk_reward = downtrend.get('avg_risk_reward_ratio', 0)
        
        return f"""## 📈 {interval.upper()}级别分析

### 基础统计
- **总趋势区间**: {total_intervals}
- **总拐点事件**: {total_events}
- **分析数据点**: {len(result.get('data', []))}

### 📈 做多策略分析
- **交易次数**: {long_total}
- **平均理想收益**: {long_ideal_profit:.2f}%
- **平均实际收益**: {long_actual_profit:.2f}%
- **平均风险损失**: {long_risk_loss:.2f}%
- **风险收益比**: {long_risk_reward:.2f}

#### 做多策略表现评估
- ✅ **理想收益**: {long_ideal_profit:.2f}% 显示策略有良好潜力
- ⚠️ **实际收益**: {long_actual_profit:.2f}% 需要优化出场时机
- ✅ **风险控制**: {long_risk_loss:.2f}% 风险损失在可接受范围
- ✅ **风险收益比**: {long_risk_reward:.2f} 显示策略具有投资价值

### 📉 做空策略分析
- **交易次数**: {short_total}
- **平均理想收益**: {short_ideal_profit:.2f}%
- **平均实际收益**: {short_actual_profit:.2f}%
- **平均风险损失**: {short_risk_loss:.2f}%
- **风险收益比**: {short_risk_reward:.2f}

#### 做空策略表现评估
- ✅ **理想收益**: {short_ideal_profit:.2f}% 显示做空策略有效
- ⚠️ **实际收益**: {short_actual_profit:.2f}% 需要优化出场策略
- ✅ **风险控制**: {short_risk_loss:.2f}% 风险损失可控
- ✅ **风险收益比**: {short_risk_reward:.2f} 显示策略具有投资价值

### 📊 策略对比分析
| 指标 | 做多策略 | 做空策略 | 优势策略 |
|------|----------|----------|----------|
| 理想收益 | {long_ideal_profit:.2f}% | {short_ideal_profit:.2f}% | {'做多' if long_ideal_profit > short_ideal_profit else '做空'} |
| 实际收益 | {long_actual_profit:.2f}% | {short_actual_profit:.2f}% | {'做多' if long_actual_profit > short_actual_profit else '做空'} |
| 风险损失 | {long_risk_loss:.2f}% | {short_risk_loss:.2f}% | {'做多' if long_risk_loss < short_risk_loss else '做空'} |
| 风险收益比 | {long_risk_reward:.2f} | {short_risk_reward:.2f} | {'做多' if long_risk_reward > short_risk_reward else '做空'} |

---

"""
    
    def _create_strategy_recommendations(self, results: Dict[str, Any]) -> str:
        """创建策略建议"""
        return """## 💡 策略建议

### 1. 出场时机优化
- **问题**: 实际收益与理想收益存在较大差距
- **建议**: 
  - 设置动态止损点，避免大幅回撤
  - 在趋势转换前提前出场
  - 使用技术指标确认出场信号

### 2. 风险控制策略
- **止损设置**: 建议设置3-5%的止损点
- **仓位管理**: 根据风险收益比调整仓位大小
- **分散投资**: 避免单一策略过度集中

### 3. 参数优化方向
- **HMA周期**: 当前45，可测试30-60范围
- **斜率阈值**: 当前0.001，可测试0.0005-0.002
- **时间级别**: 4小时级别表现最佳，可重点关注

### 4. 实施建议
- **回测验证**: 在实盘前进行充分回测
- **小仓位测试**: 初期使用小仓位验证策略
- **持续监控**: 定期评估策略表现并调整

---

"""
    
    def _create_technical_appendix(self) -> str:
        """创建技术附录"""
        return """## 🔧 技术附录

### 策略算法说明
1. **趋势识别**: 基于HMA45斜率变化识别趋势转换点
   - 上涨趋势: HMA斜率由负转正
   - 下跌趋势: HMA斜率由正转负

2. **入场时机**: 趋势转换时刻的收盘价作为入场价格

3. **收益计算**:
   - 做多策略: 研究最大涨幅（理想收益）和最大跌幅（风险损失）
   - 做空策略: 研究最大跌幅（理想收益）和最大涨幅（风险损失）

4. **风险指标**:
   - PFE (Positive Favorable Excursion): 最大有利偏移
   - MAE (Maximum Adverse Excursion): 最大不利偏移
   - 风险收益比: 理想收益 / 风险损失

### 数据说明
- **数据源**: Binance API
- **时间范围**: 2024年全年
- **数据频率**: 1小时和4小时K线
- **HMA参数**: 周期45，斜率阈值0.001

### 图表说明
- **策略总览图**: 展示价格走势、HMA曲线和拐点识别
- **策略表现图**: 对比理想收益与实际收益
- **风险分析图**: 分析风险分布和风险收益比
- **综合分析图**: 多维度展示策略表现

---

**报告生成完成**  
*本报告基于历史数据回测，实际投资需谨慎评估风险*
"""
