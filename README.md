/* ===============================================================
   📊 ENHANCED COMPACT ANALYSIS & ALERTS CSS - COMPLETE REDESIGN
   =============================================================== */

/* ==================== COMPACT GAUGE SYSTEM ==================== */
.gauges-container {
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.98), rgba(17, 24, 39, 0.98));
    border-radius: 12px;
    padding: 20px;
    margin: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(20px);
    min-height: 220px;
    display: flex;
    align-items: center;
}

.gauge-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    align-items: end;
    width: 100%;
}

.gauge-item {
    text-align: center;
    transition: all 0.3s ease;
    height: 260px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
}

.gauge-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    position: absolute;
    top: 10px;
    left: 0;
    right: 0;
    z-index: 10;
}

/* ==================== UNIFIED GAUGE SCALING ==================== */
.gauge-container {
    position: relative;
    width: 160px;
    height: 160px;
    margin: 30px auto 0;
    display: flex;
    justify-content: center;
    align-items: flex-end;
}

/* ==================== ENHANCED 270° ARC SYSTEM ==================== */
.gauge-arc {
    position: absolute;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: conic-gradient(
        from -135deg,
        rgba(255, 255, 255, 0.05) 0deg,
        rgba(255, 255, 255, 0.08) 270deg,
        transparent 270deg,
        transparent 360deg
    );
    mask: radial-gradient(circle at center, transparent 58px, black 60px);
    -webkit-mask: radial-gradient(circle at center, transparent 58px, black 60px);
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.gauge-arc-fill {
    position: absolute;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    mask: radial-gradient(circle at center, transparent 58px, black 60px);
    -webkit-mask: radial-gradient(circle at center, transparent 58px, black 60px);
    transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    filter: saturate(1.2);
}

/* ==================== ENHANCED NEEDLE SYSTEM ==================== */
.gauge-hub {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 4px solid #374151;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    z-index: 20;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
}

.gauge-needle-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 160px;
    height: 160px;
    z-index: 15;
    transform: translateX(-50%);
}

.gauge-needle {
    position: absolute;
    width: 4px;
    height: 70px;
    background: linear-gradient(to bottom, 
        #dc2626 0%,
        #ef4444 20%,
        #f8fafc 30%,
        #f8fafc 70%,
        #ef4444 80%,
        #dc2626 100%);
    transform-origin: center bottom;
    transform: translateX(-50%) rotate(-135deg);
    z-index: 15;
    transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    border-radius: 2px 2px 0 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    left: 50%;
    bottom: 50%;
}

.needle-head {
    position: absolute;
    top: -6px;
    left: 50%;
    width: 14px;
    height: 14px;
    background: radial-gradient(circle at center, #ef4444, #dc2626);
    border-radius: 50%;
    transform: translateX(-50%);
    border: 3px solid #f8fafc;
    z-index: 16;
    box-shadow: 0 0 12px rgba(239, 68, 68, 0.6);
}

/* ==================== SINGLE CENTRAL VALUE DISPLAY ==================== */
.gauge-value-container {
    position: absolute;
    bottom: -40px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    z-index: 25;
    background: rgba(31, 41, 55, 0.95);
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    min-width: 70px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.gauge-score {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.2;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2px;
}

.gauge-unit {
    font-size: 0.6rem;
    color: #9ca3af;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ==================== COMPACT LABEL CONTAINER ==================== */
.gauge-label-container {
    position: absolute;
    bottom: -65px;
    left: 10px;
    right: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    z-index: 25;
}

.gauge-label {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 5px 10px;
    border-radius: 8px;
    min-width: 65px;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.gauge-indicator-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 2px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

/* ==================== GAUGE-SPECIFIC ARC FILLS ==================== */

/* Momentum Gauge - Full Arc Always Visible */
#momentum-arc {
    background: conic-gradient(from -135deg,
        #DC2626 0deg, #EF4444 45deg, #F59E0B 90deg, 
        #22C55E 135deg, #16A34A 180deg, #15803D 225deg,
        transparent 270deg, transparent 360deg);
}

/* Risk Gauge - Partial Fill */
#risk-arc {
    background: conic-gradient(from -135deg,
        transparent 0deg,
        #22C55e 0deg, #10B981 60deg, #EAB308 120deg,
        #F97316 180deg, #EF4444 240deg, #DC2626 270deg,
        transparent 270deg);
}

/* Volatility Gauge - Partial Fill */
#volatility-arc {
    background: conic-gradient(from -135deg,
        transparent 0deg,
        #00D394 0deg, #22C55E 60deg, #EAB308 120deg,
        #F97316 180deg, #EF4444 240deg, #DC2626 270deg,
        transparent 270deg);
}

/* Strength Gauge - Partial Fill */
#strength-arc {
    background: conic-gradient(from -135deg,
        transparent 0deg,
        #DC2626 0deg, #EF4444 60deg, #EAB308 120deg,
        #22C55E 180deg, #00D394 240deg, #00B378 270deg,
        transparent 270deg);
}

/* ==================== COMPACT COLOR SYSTEM ==================== */
.gauge-label.bullish { 
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.2), rgba(0, 211, 148, 0.1));
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(0, 211, 148, 0.2);
}

.gauge-label.bearish { 
    background: linear-gradient(135deg, rgba(255, 77, 77, 0.2), rgba(255, 77, 77, 0.1));
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 77, 77, 0.2);
}

.gauge-label.neutral { 
    background: linear-gradient(135deg, rgba(148, 163, 184, 0.2), rgba(148, 163, 184, 0.1));
    color: #94A3B8; 
    border-color: rgba(148, 163, 184, 0.3);
}

.gauge-label.strong { 
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.2), rgba(0, 211, 148, 0.1));
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(0, 211, 148, 0.2);
}

.gauge-label.weak { 
    background: linear-gradient(135deg, rgba(255, 77, 77, 0.2), rgba(255, 77, 77, 0.1));
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 77, 77, 0.2);
}

.gauge-label.moderate { 
    background: linear-gradient(135deg, rgba(255, 170, 0, 0.2), rgba(255, 170, 0, 0.1));
    color: #FFAA00; 
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 170, 0, 0.2);
}

.gauge-label.high { 
    background: linear-gradient(135deg, rgba(255, 77, 77, 0.2), rgba(255, 77, 77, 0.1));
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 77, 77, 0.2);
}

.gauge-label.low { 
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.2), rgba(0, 211, 148, 0.1));
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(0, 211, 148, 0.2);
}

.gauge-label.medium { 
    background: linear-gradient(135deg, rgba(255, 170, 0, 0.2), rgba(255, 170, 0, 0.1));
    color: #FFAA00; 
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 170, 0, 0.2);
}

/* Indicator Dot Colors */
.gauge-indicator-dot.bullish { background: #00D394; border-color: #00D394; box-shadow: 0 0 10px rgba(0, 211, 148, 0.6); }
.gauge-indicator-dot.bearish { background: #FF4D4D; border-color: #FF4D4D; box-shadow: 0 0 10px rgba(255, 77, 77, 0.6); }
.gauge-indicator-dot.neutral { background: #94A3B8; border-color: #94A3B8; }
.gauge-indicator-dot.strong { background: #00D394; border-color: #00D394; box-shadow: 0 0 10px rgba(0, 211, 148, 0.6); }
.gauge-indicator-dot.weak { background: #FF4D4D; border-color: #FF4D4D; box-shadow: 0 0 10px rgba(255, 77, 77, 0.6); }
.gauge-indicator-dot.moderate { background: #FFAA00; border-color: #FFAA00; box-shadow: 0 0 10px rgba(255, 170, 0, 0.6); }
.gauge-indicator-dot.high { background: #FF4D4D; border-color: #FF4D4D; box-shadow: 0 0 10px rgba(255, 77, 77, 0.6); }
.gauge-indicator-dot.low { background: #00D394; border-color: #00D394; box-shadow: 0 0 10px rgba(0, 211, 148, 0.6); }
.gauge-indicator-dot.medium { background: #FFAA00; border-color: #FFAA00; box-shadow: 0 0 10px rgba(255, 170, 0, 0.6); }

/* ==================== RISK GAUGE PULSING ANIMATION ==================== */
.risk-high .gauge-needle {
    animation: riskPulse 1.2s ease-in-out infinite;
}

@keyframes riskPulse {
    0%, 100% { 
        filter: brightness(1) drop-shadow(0 0 15px rgba(239, 68, 68, 0.8)); 
    }
    50% { 
        filter: brightness(1.3) drop-shadow(0 0 25px rgba(239, 68, 68, 1)); 
    }
}

/* ==================== ENHANCED ANIMATIONS ==================== */
.gauge-item.extreme .gauge-needle {
    animation: needlePulse 1.5s ease-in-out infinite;
}

@keyframes needlePulse {
    0%, 100% { 
        transform: translateX(-50%) rotate(-135deg);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    50% { 
        transform: translateX(-50%) rotate(-135deg) scale(1.05);
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.6);
    }
}

.gauge-item:hover .gauge-needle {
    transform: translateX(-50%) rotate(-135deg) scale(1.02);
}

/* ==================== ANALYSIS SECTIONS ==================== */
.analysis-section {
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.98), rgba(17, 24, 39, 0.98));
    border-radius: 12px;
    padding: 18px;
    margin: 8px 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.analysis-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(0, 211, 148, 0.3), 
        transparent);
}

.analysis-section h3 {
    margin: 0 0 16px 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f8fafc;
    border-bottom: 2px solid rgba(0, 211, 148, 0.3);
    padding-bottom: 10px;
}

/* Multi-Timeframe Strength */
.timeframe-strength-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.timeframe-strength-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
}

.timeframe-strength-item:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(0, 211, 148, 0.3);
    transform: translateY(-1px);
}

.timeframe-label {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.8rem;
    color: #f8fafc;
    min-width: 35px;
}

.strength-bar-container {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 10px;
}

.strength-bar {
    flex: 1;
    height: 8px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.strength-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff4444, #ffaa00, #00cc66);
    border-radius: 4px;
    transition: width 0.5s ease;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

.strength-fill.strong { 
    background: linear-gradient(90deg, #00cc66, #00e676);
    box-shadow: 0 0 12px rgba(0, 204, 102, 0.4);
}
.strength-fill.moderate { 
    background: linear-gradient(90deg, #ffaa00, #ffbb33);
    box-shadow: 0 0 12px rgba(255, 170, 0, 0.4);
}
.strength-fill.weak { 
    background: linear-gradient(90deg, #ff4444, #ff6666);
    box-shadow: 0 0 12px rgba(255, 68, 68, 0.4);
}

.strength-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    min-width: 30px;
    text-align: right;
    color: #f8fafc;
}

.strength-value.strong { 
    color: #00cc66; 
    background: rgba(0, 204, 102, 0.1);
    border-color: rgba(0, 204, 102, 0.3);
}
.strength-value.moderate { 
    color: #ffaa00; 
    background: rgba(255, 170, 0, 0.1);
    border-color: rgba(255, 170, 0, 0.3);
}
.strength-value.weak { 
    color: #ff4444; 
    background: rgba(255, 68, 68, 0.1);
    border-color: rgba(255, 68, 68, 0.3);
}

.timeframe-direction {
    font-size: 1.1rem;
    min-width: 25px;
    text-align: center;
    transition: transform 0.3s ease;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
}

.timeframe-direction.bullish { 
    color: #00cc66; 
    text-shadow: 0 0 10px rgba(0, 204, 102, 0.6);
}
.timeframe-direction.bearish { 
    color: #ff4444; 
    text-shadow: 0 0 10px rgba(255, 68, 68, 0.6);
}

/* Indicator Consensus */
.consensus-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.consensus-meters {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.consensus-meter {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.meter-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #f1f5f9;
}

.meter-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff4444, #ffaa00, #00cc66);
    border-radius: 4px;
    transition: width 0.5s ease;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

.meter-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    color: #94a3b8;
    text-align: right;
}

.consensus-summary {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 14px;
}

.consensus-status {
    font-size: 0.85rem;
    font-weight: 600;
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.consensus-status.strong { 
    color: #00cc66; 
    background: rgba(0, 204, 102, 0.1);
    border-color: rgba(0, 204, 102, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(0, 204, 102, 0.2);
}
.consensus-status.moderate { 
    color: #ffaa00; 
    background: rgba(255, 170, 0, 0.1);
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 170, 0, 0.2);
}
.consensus-status.weak { 
    color: #ff4444; 
    background: rgba(255, 68, 68, 0.1);
    border-color: rgba(255, 68, 68, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 10px rgba(255, 68, 68, 0.2);
}

/* Market Structure */
.structure-container {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
}

.structure-levels {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.levels-group h4 {
    margin: 0 0 8px 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: #f8fafc;
    padding-bottom: 6px;
    border-bottom: 1px solid;
}

.levels-group:first-child h4 { 
    color: #FF4D4D; 
    border-bottom-color: rgba(255, 77, 77, 0.3);
}
.levels-group:last-child h4 { 
    color: #00D394; 
    border-bottom-color: rgba(0, 211, 148, 0.3);
}

.levels-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.level-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 8px 10px;
    border-radius: 6px;
    border: 1px solid;
    text-align: center;
    font-weight: 600;
    transition: all 0.3s ease;
}

.level-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.level-item.resistance {
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D;
    border-color: rgba(255, 77, 77, 0.2);
}

.level-item.support {
    background: rgba(0, 211, 148, 0.1);
    color: #00D394;
    border-color: rgba(0, 211, 148, 0.2);
}

.structure-trend {
    display: flex;
    flex-direction: column;
    gap: 12px;
    justify-content: center;
}

.trend-indicator {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.trend-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #f1f5f9;
}

.trend-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 6px;
    border: 1px solid;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.trend-value.bullish { 
    background: rgba(0, 211, 148, 0.1);
    color: #00D394;
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(0, 211, 148, 0.2);
}
.trend-value.bearish { 
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D;
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(255, 77, 77, 0.2);
}
.trend-value.neutral { 
    background: rgba(148, 163, 184, 0.1);
    color: #94A3B8;
    border-color: rgba(148, 163, 184, 0.3);
}

.trend-strength {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.trend-bar {
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.trend-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff4444, #ffaa00, #00cc66);
    border-radius: 3px;
    transition: width 0.5s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* Trading Setups */
.setups-container {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
}

.setup-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
}

.setup-card {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    padding: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
}

.setup-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    border-color: rgba(255, 255, 255, 0.15);
}

.setup-card.long {
    border-left: 3px solid #00D394;
    background: rgba(0, 211, 148, 0.05);
}

.setup-card.short {
    border-left: 3px solid #FF4D4D;
    background: rgba(255, 77, 77, 0.05);
}

.setup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.setup-type {
    font-size: 0.75rem;
    font-weight: 600;
    color: #f8fafc;
}

.setup-confidence {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 10px;
    border: 1px solid;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.setup-confidence.high { 
    background: rgba(0, 211, 148, 0.15);
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(0, 211, 148, 0.2);
}
.setup-confidence.medium { 
    background: rgba(255, 170, 0, 0.15);
    color: #FFAA00; 
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(255, 170, 0, 0.2);
}
.setup-confidence.low { 
    background: rgba(255, 77, 77, 0.15);
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(255, 77, 77, 0.2);
}

.setup-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.setup-direction {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 5px 8px;
    border-radius: 5px;
    text-align: center;
    text-transform: uppercase;
    border: 1px solid;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.setup-direction.long { 
    background: rgba(0, 211, 148, 0.15);
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(0, 211, 148, 0.2);
}
.setup-direction.short { 
    background: rgba(255, 77, 77, 0.15);
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(255, 77, 77, 0.2);
}

.setup-metrics {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.metric-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-item:last-child {
    border-bottom: none;
}

.metric-label {
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 600;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: #f8fafc;
}

.no-setups {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    padding: 20px;
    font-style: italic;
    grid-column: 1 / -1;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Volume Analysis */
.volume-container {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 16px;
}

.volume-metrics {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.volume-metric {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
}

.volume-metric:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(0, 211, 148, 0.3);
    transform: translateY(-1px);
}

.volume-label {
    font-size: 0.7rem;
    color: #94a3b8;
    font-weight: 600;
}

.volume-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: #f8fafc;
    padding: 4px 8px;
    border-radius: 5px;
    border: 1px solid;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.volume-value.increasing { 
    background: rgba(0, 211, 148, 0.1);
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(0, 211, 148, 0.2);
}
.volume-value.decreasing { 
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(255, 77, 77, 0.2);
}
.volume-value.neutral { 
    background: rgba(148, 163, 184, 0.1);
    color: #94A3B8; 
    border-color: rgba(148, 163, 184, 0.3);
}
.volume-value.strong { 
    background: rgba(0, 211, 148, 0.1);
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(0, 211, 148, 0.2);
}
.volume-value.weak { 
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), 0 0 8px rgba(255, 77, 77, 0.2);
}

.volume-bars {
    display: flex;
    align-items: end;
    gap: 10px;
    height: 100px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.volume-bar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    flex: 1;
}

.volume-bar-label {
    font-size: 0.65rem;
    color: #94a3b8;
    font-weight: 600;
}

.volume-bar {
    flex: 1;
    width: 16px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: end;
    overflow: hidden;
}

.volume-bar-fill {
    width: 100%;
    background: linear-gradient(to top, #ff4444, #ffaa00, #00cc66);
    border-radius: 8px;
    transition: height 0.5s ease;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

/* ==================== ALERTS STYLING ==================== */
.alerts-container {
    padding: 20px;
    max-width: 1000px;
    margin: 0 auto;
    background: transparent;
}

.alert-item {
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.98), rgba(17, 24, 39, 0.98));
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    border-left: 4px solid #FF9900;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.4s ease;
    backdrop-filter: blur(20px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.alert-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.2), 
        transparent);
}

.alert-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.15);
}

.alert-item.active {
    border-left-color: #FF0000;
    background: linear-gradient(135deg, rgba(255, 0, 0, 0.12), rgba(255, 0, 0, 0.06));
}

.alert-item.resolved {
    border-left-color: #00FF00;
    background: linear-gradient(135deg, rgba(0, 255, 0, 0.12), rgba(0, 255, 0, 0.06));
    opacity: 0.7;
}

.alert-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.alert-type {
    font-weight: 700;
    font-size: 0.75rem;
    padding: 6px 12px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    backdrop-filter: blur(20px);
    border: 1px solid;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.alert-time {
    font-size: 0.7rem;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

.alert-message {
    font-size: 0.85rem;
    margin-bottom: 12px;
    line-height: 1.5;
    color: #f8fafc;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.alert-actions {
    display: flex;
    gap: 8px;
}

.alert-btn {
    padding: 8px 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: linear-gradient(135deg, rgba(31, 41, 55, 0.9), rgba(17, 24, 39, 0.85));
    color: #f8fafc;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.3s ease;
    font-weight: 600;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.alert-btn:hover {
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.2), rgba(0, 211, 148, 0.1));
    border-color: rgba(0, 211, 148, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.alert-btn.resolve {
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.2), rgba(0, 211, 148, 0.1));
    border-color: rgba(0, 211, 148, 0.3);
    color: #00D394;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(0, 211, 148, 0.2);
}

.alert-btn.test {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
    border-color: rgba(59, 130, 246, 0.3);
    color: #3B82F6;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(59, 130, 246, 0.2);
}

.alert-btn.clear {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
    border-color: rgba(239, 68, 68, 0.3);
    color: #EF4444;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(239, 68, 68, 0.2);
}

.alert-setting-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.alert-setting-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.alert-setting-item:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(0, 211, 148, 0.3);
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.alert-setting-item input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: #00D394;
    filter: drop-shadow(0 2px 4px rgba(0, 211, 148, 0.3));
}

.alert-setting-item label {
    font-size: 0.8rem;
    color: #f8fafc;
    cursor: pointer;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.alert-actions-global {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    justify-content: center;
}

.no-alerts {
    text-align: center;
    padding: 40px;
    color: #94a3b8;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

.no-alerts-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
    opacity: 0.5;
    filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.3));
}

.no-alerts-text {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 6px;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
}

.no-alerts-subtext {
    font-size: 0.8rem;
    opacity: 0.7;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

/* Alert Type Colors */
.alert-item.momentum { 
    border-left: 4px solid #3A86FF; 
    background: linear-gradient(135deg, rgba(58, 134, 255, 0.12), rgba(58, 134, 255, 0.06));
}

.alert-item.volatility { 
    border-left: 4px solid #FFAA00; 
    background: linear-gradient(135deg, rgba(255, 170, 0, 0.12), rgba(255, 170, 0, 0.06));
}

.alert-item.strength { 
    border-left: 4px solid #00D394; 
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.12), rgba(0, 211, 148, 0.06));
}

.alert-item.risk { 
    border-left: 4px solid #FF4D4D; 
    background: linear-gradient(135deg, rgba(255, 77, 77, 0.12), rgba(255, 77, 77, 0.06));
}

.alert-item.rsi { 
    border-left: 4px solid #F59E0B; 
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(245, 158, 11, 0.06));
}

.alert-item.volume { 
    border-left: 4px solid #8B5CF6; 
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(139, 92, 246, 0.06));
}

.alert-item.price { 
    border-left: 4px solid #EC4899; 
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.12), rgba(236, 72, 153, 0.06));
}

.alert-item.test { 
    border-left: 4px solid #6B7280; 
    background: linear-gradient(135deg, rgba(107, 114, 128, 0.12), rgba(107, 114, 128, 0.06));
}

.alert-item.momentum .alert-type { 
    background: linear-gradient(135deg, rgba(58, 134, 255, 0.2), rgba(58, 134, 255, 0.1));
    color: #3A86FF; 
    border-color: rgba(58, 134, 255, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(58, 134, 255, 0.2);
}

.alert-item.volatility .alert-type { 
    background: linear-gradient(135deg, rgba(255, 170, 0, 0.2), rgba(255, 170, 0, 0.1));
    color: #FFAA00; 
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(255, 170, 0, 0.2);
}

.alert-item.strength .alert-type { 
    background: linear-gradient(135deg, rgba(0, 211, 148, 0.2), rgba(0, 211, 148, 0.1));
    color: #00D394; 
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(0, 211, 148, 0.2);
}

.alert-item.risk .alert-type { 
    background: linear-gradient(135deg, rgba(255, 77, 77, 0.2), rgba(255, 77, 77, 0.1));
    color: #FF4D4D; 
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(255, 77, 77, 0.2);
}

.alert-item.rsi .alert-type { 
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
    color: #F59E0B; 
    border-color: rgba(245, 158, 11, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(245, 158, 11, 0.2);
}

.alert-item.volume .alert-type { 
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1));
    color: #8B5CF6; 
    border-color: rgba(139, 92, 246, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(139, 92, 246, 0.2);
}

.alert-item.price .alert-type { 
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(236, 72, 153, 0.1));
    color: #EC4899; 
    border-color: rgba(236, 72, 153, 0.3);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 10px rgba(236, 72, 153, 0.2);
}

.alert-item.test .alert-type { 
    background: linear-gradient(135deg, rgba(107, 114, 128, 0.2), rgba(107, 114, 128, 0.1));
    color: #6B7280; 
    border-color: rgba(107, 114, 128, 0.3);
}

/* ==================== SUMMARY CONTENT ==================== */
.summary-content {
    display: grid;
    gap: 12px;
    margin-top: 16px;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.summary-item:hover {
    transform: translateY(-1px);
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.summary-item .label {
    font-weight: 600;
    color: #f1f5f9;
    font-size: 0.85rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.summary-item .value {
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    padding: 6px 12px;
    border-radius: 8px;
    backdrop-filter: blur(20px);
    border: 1px solid;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
}

.summary-item .value.bullish { 
    background: rgba(0, 211, 148, 0.1);
    color: #00D394;
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(0, 211, 148, 0.2);
}

.summary-item .value.bearish { 
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D;
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 77, 77, 0.2);
}

.summary-item .value.neutral { 
    background: rgba(148, 163, 184, 0.1);
    color: #94A3B8;
    border-color: rgba(148, 163, 184, 0.3);
}

.summary-item .value.strong { 
    background: rgba(0, 211, 148, 0.1);
    color: #00D394;
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(0, 211, 148, 0.2);
}

.summary-item .value.weak { 
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D;
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 77, 77, 0.2);
}

.summary-item .value.moderate { 
    background: rgba(255, 170, 0, 0.1);
    color: #FFAA00;
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 170, 0, 0.2);
}

.summary-item .value.high { 
    background: rgba(255, 77, 77, 0.1);
    color: #FF4D4D;
    border-color: rgba(255, 77, 77, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 77, 77, 0.2);
}

.summary-item .value.low { 
    background: rgba(0, 211, 148, 0.1);
    color: #00D394;
    border-color: rgba(0, 211, 148, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(0, 211, 148, 0.2);
}

.summary-item .value.medium { 
    background: rgba(255, 170, 0, 0.1);
    color: #FFAA00;
    border-color: rgba(255, 170, 0, 0.3);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 170, 0, 0.2);
}

/* ==================== RESPONSIVE DESIGN ==================== */
@media (max-width: 1200px) {
    .gauge-row {
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }
    
    .gauges-container {
        min-height: 280px;
    }
    
    .gauge-item {
        height: 260px;
    }
    
    .consensus-container {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .structure-container {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .setups-container {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .volume-container {
        grid-template-columns: 1fr;
        gap: 12px;
    }
}

@media (max-width: 768px) {
    .gauge-row {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .gauges-container {
        margin: 8px;
        padding: 16px;
        min-height: auto;
    }
    
    .gauge-item {
        height: 260px;
    }
    
    .analysis-section {
        margin: 6px 8px;
        padding: 14px;
    }
    
    .structure-levels {
        grid-template-columns: 1fr;
        gap: 10px;
    }
    
    .setup-cards {
        grid-template-columns: 1fr;
    }
    
    .volume-bars {
        height: 80px;
        padding: 10px;
    }
    
    .volume-bar {
        width: 14px;
    }
    
    .gauge-container {
        width: 140px;
        height: 140px;
    }
    
    .gauge-arc,
    .gauge-arc-fill {
        width: 140px;
        height: 140px;
    }
    
    .gauge-needle-container {
        width: 140px;
        height: 140px;
    }
}

@media (max-width: 480px) {
    .gauges-container {
        padding: 12px;
    }
    
    .gauge-container {
        width: 120px;
        height: 120px;
    }
    
    .gauge-arc,
    .gauge-arc-fill {
        width: 120px;
        height: 120px;
    }
    
    .gauge-needle-container {
        width: 120px;
        height: 120px;
    }
    
    .gauge-value-container {
        padding: 6px 12px;
    }
    
    .gauge-score {
        font-size: 0.9rem;
    }
    
    .alert-actions {
        flex-direction: column;
    }
    
    .alert-btn {
        width: 100%;
        text-align: center;
    }
}