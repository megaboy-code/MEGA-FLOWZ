# ===============================================================
# 📊🔔 ANALYSIS_ALERTS.JS - PROFESSIONAL ENHANCED VERSION
# ===============================================================

// Analysis state
let currentAnalysis = {};
let activeAlerts = [];
let alertSettings = {
    rsiAlerts: true,
    priceAlerts: false,
    volumeAlerts: true,
    momentumAlerts: true
};

// Gauge state
let gaugeValues = {
    momentum: 50,
    volatility: 50,
    strength: 50,
    risk: 50
};

// Initialize analysis & alerts module
function initializeAnalysisAlerts() {
    console.log("📊🔔 Enhanced Analysis & Alerts module initialized");
    loadAlertSettings();
    createGaugeComponents();
    initializeEnhancedAnalysis();
    renderAnalysisSections();
    renderAlertsSections();
}

// ==================== CONFLUENCE CALCULATION ENGINE ====================

// Calculate confluence from pyramid data
function calculateConfluence(pyramidData) {
    if (!pyramidData || !pyramidData.blocks) {
        return gaugeValues;
    }
    
    const analysis = {
        timeframeMomentum: [],
        timeframeVolatility: [],
        indicatorConsensus: [],
        volumeAnalysis: []
    };
    
    // Analyze each timeframe block
    pyramidData.blocks.forEach(block => {
        const blockAnalysis = analyzeTimeframeBlock(block);
        analysis.timeframeMomentum.push(blockAnalysis.momentum);
        analysis.timeframeVolatility.push(blockAnalysis.volatility);
        analysis.indicatorConsensus.push(blockAnalysis.indicatorScore);
        analysis.volumeAnalysis.push(blockAnalysis.volumeStrength);
    });
    
    // Calculate gauge values
    gaugeValues.momentum = calculateMomentumConfluence(analysis.timeframeMomentum);
    gaugeValues.volatility = calculateVolatilityConfluence(analysis.timeframeVolatility);
    gaugeValues.strength = calculateStrengthConfluence(analysis);
    gaugeValues.risk = calculateRiskAssessment(analysis);
    
    updateGauges();
    return gaugeValues;
}

// Analyze individual timeframe block
function analyzeTimeframeBlock(block) {
    const analysis = {
        momentum: 0,
        volatility: 0,
        indicatorScore: 0,
        volumeStrength: 0
    };
    
    // Momentum analysis (from block data)
    if (block.dir === '🟢') analysis.momentum = 1;
    else if (block.dir === '🔴') analysis.momentum = -1;
    
    // Volatility analysis (placeholder - would use ATR data)
    analysis.volatility = Math.random() * 100; // Replace with real ATR calculation
    
    // Indicator consensus (from momentum summary)
    analysis.indicatorScore = analyzeMomentumSummary(block.momentum_summary);
    
    // Volume strength (from volume data)
    analysis.volumeStrength = block.volume > 1000 ? 1 : 0.5;
    
    return analysis;
}

// Analyze momentum summary text
function analyzeMomentumSummary(summary) {
    if (!summary) return 50;
    
    let score = 50;
    
    // Basic sentiment analysis from summary text
    if (summary.includes('Strong') || summary.includes('++')) score += 25;
    if (summary.includes('Weak') || summary.includes('--')) score -= 25;
    if (summary.includes('🟢')) score += 15;
    if (summary.includes('🔴')) score -= 15;
    
    return Math.max(0, Math.min(100, score));
}

// Calculate momentum confluence
function calculateMomentumConfluence(momentumScores) {
    if (momentumScores.length === 0) return 50;
    
    // Weight recent timeframes more heavily
    const weights = [0.3, 0.25, 0.2, 0.15, 0.1]; // D1, H4, H1, M15, M5 weights
    let weightedSum = 0;
    let totalWeight = 0;
    
    momentumScores.forEach((score, index) => {
        const weight = weights[index] || 0.1;
        weightedSum += (score + 1) * 50 * weight; // Convert -1/1 to 0-100 scale
        totalWeight += weight;
    });
    
    return Math.round(weightedSum / totalWeight);
}

// Calculate volatility confluence
function calculateVolatilityConfluence(volatilityScores) {
    if (volatilityScores.length === 0) return 50;
    return Math.round(volatilityScores.reduce((a, b) => a + b, 0) / volatilityScores.length);
}

// Calculate strength confluence
function calculateStrengthConfluence(analysis) {
    const momentumStrength = gaugeValues.momentum;
    const consensusStrength = analysis.indicatorConsensus.reduce((a, b) => a + b, 0) / analysis.indicatorConsensus.length;
    const volumeStrength = analysis.volumeAnalysis.reduce((a, b) => a + b, 0) / analysis.volumeAnalysis.length * 100;
    
    // Weighted average of all strength factors
    return Math.round(
        (momentumStrength * 0.4) + 
        (consensusStrength * 0.4) + 
        (volumeStrength * 0.2)
    );
}

// Calculate risk assessment
function calculateRiskAssessment(analysis) {
    const volatilityRisk = gaugeValues.volatility > 70 ? 80 : gaugeValues.volatility > 30 ? 50 : 20;
    const momentumRisk = Math.abs(gaugeValues.momentum - 50) > 30 ? 70 : 40;
    const consensusRisk = analysis.indicatorConsensus.some(score => score < 30) ? 60 : 30;
    
    return Math.round((volatilityRisk + momentumRisk + consensusRisk) / 3);
}

// ==================== PROFESSIONAL GAUGE COMPONENTS ====================

// Create professional gauge components
function createGaugeComponents() {
    const analysisContainer = document.getElementById('analysis-tab');
    if (!analysisContainer) return;
    
    // Add gauges container if it doesn't exist
    if (!document.getElementById('gauges-container')) {
        const gaugesHTML = `
            <div class="gauges-container" id="gauges-container">
                <div class="gauge-row">
                    <div class="gauge-item">
                        <div class="gauge-title">Momentum</div>
                        ${createProfessionalGaugeLayer('momentum', 50)}
                    </div>
                    
                    <div class="gauge-item">
                        <div class="gauge-title">Volatility</div>
                        ${createProfessionalGaugeLayer('volatility', 50)}
                    </div>
                    
                    <div class="gauge-item">
                        <div class="gauge-title">Strength</div>
                        ${createProfessionalGaugeLayer('strength', 50)}
                    </div>
                    
                    <div class="gauge-item">
                        <div class="gauge-title">Risk</div>
                        ${createProfessionalGaugeLayer('risk', 50)}
                    </div>
                </div>
            </div>
        `;
        
        analysisContainer.insertAdjacentHTML('afterbegin', gaugesHTML);
    }
}

// ------------------------------------------------------------
//  PROFESSIONAL GAUGE LAYER - Enhanced Visual Design
// ------------------------------------------------------------
function createProfessionalGaugeLayer(type, value) {
    return `
        <div class="gauge-container">
            <!-- Background Arc -->
            <div class="gauge-arc">
                <div class="gauge-arc-fill" id="${type}-arc"></div>
            </div>
            
            <!-- Center Hub -->
            <div class="gauge-hub"></div>
            
            <!-- Needle with smooth pivot -->
            <div class="gauge-needle-container">
                <div class="gauge-needle" id="${type}-needle">
                    <div class="needle-head"></div>
                </div>
            </div>
            
            <!-- Value Display -->
            <div class="gauge-value-container">
                <div class="gauge-score" id="${type}-score">${Math.round(value)}</div>
                <div class="gauge-unit">%</div>
            </div>
            
            <!-- Label with colored indicator -->
            <div class="gauge-label-container">
                <div class="gauge-label" id="${type}-label"></div>
                <div class="gauge-indicator-dot" id="${type}-indicator"></div>
            </div>
            
            <!-- Threshold Markers -->
            <div class="gauge-markers">
                <div class="marker marker-0">0</div>
                <div class="marker marker-25">25</div>
                <div class="marker marker-50">50</div>
                <div class="marker marker-75">75</div>
                <div class="marker marker-100">100</div>
            </div>
        </div>
    `;
}

// ------------------------------------------------------------
//  ENHANCED GAUGE UPDATE WITH SMOOTH ANIMATIONS
// ------------------------------------------------------------
function updateGauge(type, value) {
    const needle = document.getElementById(`${type}-needle`);
    const scoreEl = document.getElementById(`${type}-score`);
    const labelEl = document.getElementById(`${type}-label`);
    const arcEl = document.getElementById(`${type}-arc`);
    const indicatorEl = document.getElementById(`${type}-indicator`);

    if (!needle || !scoreEl || !labelEl || !arcEl || !indicatorEl) return;

    // Smooth value transition
    const currentValue = parseInt(scoreEl.textContent) || 0;
    const valueDiff = Math.abs(value - currentValue);
    const transitionTime = Math.min(1000, valueDiff * 10); // Dynamic timing

    // Apply smooth transitions
    needle.style.transition = `transform ${transitionTime}ms cubic-bezier(0.34, 1.56, 0.64, 1)`;
    arcEl.style.transition = `background ${transitionTime}ms ease-out`;
    indicatorEl.style.transition = `background ${transitionTime}ms ease-out`;

    // 1. Needle rotation (-135° to +135°)
    const rotation = (value / 100) * 270 - 135;
    needle.style.transform = `translateX(-50%) rotate(${rotation}deg)`;

    // 2. Score with counting animation
    animateValue(scoreEl, currentValue, value, transitionTime);

    // 3. Dynamic arc color
    updateGaugeArc(type, value, arcEl);

    // 4. Label + Color with indicator
    updateGaugeLabelWithColor(type, value, labelEl, indicatorEl);
}

// ------------------------------------------------------------
//  SMOOTH VALUE COUNTING ANIMATION
// ------------------------------------------------------------
function animateValue(element, start, end, duration) {
    const startTime = performance.now();
    const change = end - start;

    function updateValue(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth counting
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const currentValue = Math.round(start + change * easeOut);
        
        element.textContent = currentValue;

        if (progress < 1) {
            requestAnimationFrame(updateValue);
        }
    }

    requestAnimationFrame(updateValue);
}

// ------------------------------------------------------------
//  DYNAMIC GAUGE ARC COLOR
// ------------------------------------------------------------
function updateGaugeArc(type, value, arcEl) {
    const hue = value >= 50 ? 
        120 + (value - 50) * 1.2 : // Green to brighter green (50-100)
        30 - (50 - value) * 0.6;   // Orange to red (0-50)
    
    const saturation = 85;
    const lightness = value >= 50 ? 
        40 + (value - 50) * 0.3 :  // Darker to lighter green
        50 - (50 - value) * 0.2;   // Lighter to darker red

    arcEl.style.background = `conic-gradient(
        from -135deg,
        hsl(${hue}, ${saturation}%, ${lightness}%) 0%,
        hsl(${hue}, ${saturation}%, ${lightness}%) ${value}%,
        rgba(255, 255, 255, 0.1) ${value}%,
        rgba(255, 255, 255, 0.1) 100%
    )`;
}

// ------------------------------------------------------------
//  ENHANCED LABEL WITH INDICATOR DOT
// ------------------------------------------------------------
function updateGaugeLabelWithColor(type, value, labelEl, indicatorEl) {
    value = Math.max(0, Math.min(100, value));

    const CONFIG = {
        momentum: {
            thresholds: [0, 15, 30, 45, 55, 70, 85, 100],
            labels: ['Extreme Bear','Strong Bear','Bearish','Neutral','Bullish','Strong Bull','Extreme Bull'],
            colors: ['#dc2626', '#ef4444', '#f87171', '#9ca3af', '#60a5fa', '#3b82f6', '#1d4ed8']
        },
        volatility: {
            thresholds: [0, 20, 40, 60, 80, 100],
            labels: ['Very Low', 'Low', 'Medium', 'High', 'Extreme'],
            colors: ['#16a34a', '#22c55e', '#eab308', '#f97316', '#dc2626']
        },
        strength: {
            thresholds: [0, 20, 40, 60, 80, 100],
            labels: ['Very Weak', 'Weak', 'Moderate', 'Strong', 'Very Strong'],
            colors: ['#dc2626', '#ef4444', '#eab308', '#22c55e', '#16a34a']
        },
        risk: {
            thresholds: [0, 20, 40, 60, 80, 100],
            labels: ['Very Low', 'Low', 'Medium', 'High', 'Very High'],
            colors: ['#16a34a', '#22c55e', '#eab308', '#f97316', '#dc2626']
        }
    };

    const cfg = CONFIG[type];
    if (!cfg) { 
        labelEl.textContent = '—'; 
        indicatorEl.style.background = '#9ca3af';
        return; 
    }

    // Find appropriate bucket
    let idx = cfg.thresholds.length - 1;
    for (let i = 0; i < cfg.thresholds.length - 1; i++) {
        if (value < cfg.thresholds[i + 1]) { 
            idx = i; 
            break; 
        }
    }

    labelEl.textContent = cfg.labels[idx];
    labelEl.style.color = cfg.colors[idx];
    indicatorEl.style.background = cfg.colors[idx];
    
    // Add glow effect for extreme values
    if (value >= 85 || value <= 15) {
        indicatorEl.style.boxShadow = `0 0 8px ${cfg.colors[idx]}80`;
    } else {
        indicatorEl.style.boxShadow = 'none';
    }
}

// Update all gauges with professional animations
function updateGauges() {
    updateGauge('momentum', gaugeValues.momentum);
    updateGauge('volatility', gaugeValues.volatility);
    updateGauge('strength', gaugeValues.strength);
    updateGauge('risk', gaugeValues.risk);
}

// ==================== ENHANCED ANALYSIS COMPONENTS ====================

// Initialize enhanced analysis components
function initializeEnhancedAnalysis() {
    createMultiTimeframePanel();
    createIndicatorConsensusPanel();
    createMarketStructurePanel();
    createTradingSetupPanel();
    createVolumeAnalysisPanel();
}

// Create multi-timeframe strength panel
function createMultiTimeframePanel() {
    const analysisContainer = document.getElementById('analysis-tab');
    if (!analysisContainer) return;
    
    const timeframeHTML = `
        <div class="analysis-section" id="timeframe-strength-section">
            <h3>📈 Multi-Timeframe Strength</h3>
            <div class="timeframe-strength-container" id="timeframe-strength-container">
                <!-- Timeframe strength bars will be populated here -->
            </div>
        </div>
    `;
    
    // Insert after gauges container
    const gaugesContainer = document.getElementById('gauges-container');
    if (gaugesContainer) {
        gaugesContainer.insertAdjacentHTML('afterend', timeframeHTML);
    }
}

// Create indicator consensus panel
function createIndicatorConsensusPanel() {
    const analysisContainer = document.getElementById('analysis-tab');
    if (!analysisContainer) return;
    
    const consensusHTML = `
        <div class="analysis-section" id="indicator-consensus-section">
            <h3>🎯 Indicator Consensus</h3>
            <div class="consensus-container" id="consensus-container">
                <div class="consensus-meters">
                    <div class="consensus-meter">
                        <div class="meter-label">Trend Indicators</div>
                        <div class="meter-bar">
                            <div class="meter-fill" id="trend-consensus-fill" style="width: 0%"></div>
                        </div>
                        <div class="meter-value" id="trend-consensus-value">0%</div>
                    </div>
                    <div class="consensus-meter">
                        <div class="meter-label">Momentum Indicators</div>
                        <div class="meter-bar">
                            <div class="meter-fill" id="momentum-consensus-fill" style="width: 0%"></div>
                        </div>
                        <div class="meter-value" id="momentum-consensus-value">0%</div>
                    </div>
                    <div class="consensus-meter">
                        <div class="meter-label">Volatility Indicators</div>
                        <div class="meter-bar">
                            <div class="meter-fill" id="volatility-consensus-fill" style="width: 0%"></div>
                        </div>
                        <div class="meter-value" id="volatility-consensus-value">0%</div>
                    </div>
                </div>
                <div class="consensus-summary" id="consensus-summary">
                    <div class="consensus-status">Analyzing indicator alignment...</div>
                </div>
            </div>
        </div>
    `;
    
    const timeframeSection = document.getElementById('timeframe-strength-section');
    if (timeframeSection) {
        timeframeSection.insertAdjacentHTML('afterend', consensusHTML);
    }
}

// Create market structure panel
function createMarketStructurePanel() {
    const analysisContainer = document.getElementById('analysis-tab');
    if (!analysisContainer) return;
    
    const structureHTML = `
        <div class="analysis-section" id="market-structure-section">
            <h3>🏗️ Market Structure</h3>
            <div class="structure-container" id="structure-container">
                <div class="structure-levels">
                    <div class="levels-group">
                        <h4>Resistance Levels</h4>
                        <div class="levels-list" id="resistance-levels">
                            <!-- Resistance levels will be populated here -->
                        </div>
                    </div>
                    <div class="levels-group">
                        <h4>Support Levels</h4>
                        <div class="levels-list" id="support-levels">
                            <!-- Support levels will be populated here -->
                        </div>
                    </div>
                </div>
                <div class="structure-trend">
                    <div class="trend-indicator">
                        <span class="trend-label">Primary Trend:</span>
                        <span class="trend-value" id="primary-trend">Analyzing...</span>
                    </div>
                    <div class="trend-strength">
                        <span class="trend-label">Trend Strength:</span>
                        <div class="trend-bar">
                            <div class="trend-fill" id="trend-strength-fill" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const consensusSection = document.getElementById('indicator-consensus-section');
    if (consensusSection) {
        consensusSection.insertAdjacentHTML('afterend', structureHTML);
    }
}

// Create trading setup panel
function createTradingSetupPanel() {
    const analysisContainer = document.getElementById('analysis-tab');
    if (!analysisContainer) return;
    
    const setupHTML = `
        <div class="analysis-section" id="trading-setup-section">
            <h3>💰 Trading Setups</h3>
            <div class="setups-container" id="setups-container">
                <div class="setup-cards" id="setup-cards">
                    <!-- Trading setup cards will be populated here -->
                </div>
                <div class="setup-metrics">
                    <div class="metric-item">
                        <span class="metric-label">Avg. Risk/Reward:</span>
                        <span class="metric-value" id="avg-risk-reward">1:1.5</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Success Probability:</span>
                        <span class="metric-value" id="success-probability">65%</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Market Condition:</span>
                        <span class="metric-value" id="market-condition">Trending</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const structureSection = document.getElementById('market-structure-section');
    if (structureSection) {
        structureSection.insertAdjacentHTML('afterend', setupHTML);
    }
}

// Create volume analysis panel
function createVolumeAnalysisPanel() {
    const analysisContainer = document.getElementById('analysis-tab');
    if (!analysisContainer) return;
    
    const volumeHTML = `
        <div class="analysis-section" id="volume-analysis-section">
            <h3>📊 Volume Analysis</h3>
            <div class="volume-container" id="volume-container">
                <div class="volume-metrics">
                    <div class="volume-metric">
                        <div class="volume-label">Volume Trend</div>
                        <div class="volume-value" id="volume-trend">Neutral</div>
                    </div>
                    <div class="volume-metric">
                        <div class="volume-label">Volume vs Avg</div>
                        <div class="volume-value" id="volume-vs-avg">+15%</div>
                    </div>
                    <div class="volume-metric">
                        <div class="volume-label">Volume Confirmation</div>
                        <div class="volume-value" id="volume-confirmation">Strong</div>
                    </div>
                </div>
                <div class="volume-bars">
                    <div class="volume-bar-container">
                        <div class="volume-bar-label">D1</div>
                        <div class="volume-bar">
                            <div class="volume-bar-fill" id="volume-d1" style="height: 0%"></div>
                        </div>
                    </div>
                    <div class="volume-bar-container">
                        <div class="volume-bar-label">H4</div>
                        <div class="volume-bar">
                            <div class="volume-bar-fill" id="volume-h4" style="height: 0%"></div>
                        </div>
                    </div>
                    <div class="volume-bar-container">
                        <div class="volume-bar-label">H1</div>
                        <div class="volume-bar">
                            <div class="volume-bar-fill" id="volume-h1" style="height: 0%"></div>
                        </div>
                    </div>
                    <div class="volume-bar-container">
                        <div class="volume-bar-label">M15</div>
                        <div class="volume-bar">
                            <div class="volume-bar-fill" id="volume-m15" style="height: 0%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const setupSection = document.getElementById('trading-setup-section');
    if (setupSection) {
        setupSection.insertAdjacentHTML('afterend', volumeHTML);
    }
}

// ==================== ENHANCED ANALYSIS UPDATES ====================

// Update all enhanced analysis components
function updateEnhancedAnalysis(pyramidData, chartData) {
    updateMultiTimeframeStrength(pyramidData);
    updateIndicatorConsensus(pyramidData);
    updateMarketStructure(chartData);
    updateTradingSetups(pyramidData, chartData);
    updateVolumeAnalysis(pyramidData);
}

// Update multi-timeframe strength bars
function updateMultiTimeframeStrength(pyramidData) {
    const container = document.getElementById('timeframe-strength-container');
    if (!container || !pyramidData.blocks) return;
    
    let strengthHTML = '';
    pyramidData.blocks.forEach((block, index) => {
        const strength = calculateTimeframeStrength(block);
        const strengthPercent = Math.round(strength * 100);
        const strengthClass = getStrengthClass(strengthPercent);
        
        strengthHTML += `
            <div class="timeframe-strength-item">
                <div class="timeframe-label">${block.tf}</div>
                <div class="strength-bar-container">
                    <div class="strength-bar">
                        <div class="strength-fill ${strengthClass}" style="width: ${strengthPercent}%"></div>
                    </div>
                    <div class="strength-value ${strengthClass}">${strengthPercent}%</div>
                </div>
                <div class="timeframe-direction ${block.dir === '🟢' ? 'bullish' : 'bearish'}">
                    ${block.dir}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = strengthHTML;
}

// Update indicator consensus
function updateIndicatorConsensus(pyramidData) {
    const consensus = calculateIndicatorConsensus(pyramidData);
    
    // Update trend consensus
    document.getElementById('trend-consensus-fill').style.width = consensus.trend + '%';
    document.getElementById('trend-consensus-value').textContent = consensus.trend + '%';
    
    // Update momentum consensus
    document.getElementById('momentum-consensus-fill').style.width = consensus.momentum + '%';
    document.getElementById('momentum-consensus-value').textContent = consensus.momentum + '%';
    
    // Update volatility consensus
    document.getElementById('volatility-consensus-fill').style.width = consensus.volatility + '%';
    document.getElementById('volatility-consensus-value').textContent = consensus.volatility + '%';
    
    // Update consensus summary
    const summaryElement = document.getElementById('consensus-summary');
    if (summaryElement) {
        const overallConsensus = Math.round((consensus.trend + consensus.momentum + consensus.volatility) / 3);
        const consensusClass = getConsensusClass(overallConsensus);
        summaryElement.innerHTML = `
            <div class="consensus-status ${consensusClass}">
                Overall Consensus: ${overallConsensus}% - ${getConsensusText(overallConsensus)}
            </div>
        `;
    }
}

// Update market structure
function updateMarketStructure(chartData) {
    const structure = analyzeMarketStructure(chartData);
    
    // Update resistance levels
    const resistanceElement = document.getElementById('resistance-levels');
    if (resistanceElement) {
        resistanceElement.innerHTML = structure.resistanceLevels.map(level => 
            `<div class="level-item resistance">${level.toFixed(5)}</div>`
        ).join('');
    }
    
    // Update support levels
    const supportElement = document.getElementById('support-levels');
    if (supportElement) {
        supportElement.innerHTML = structure.supportLevels.map(level => 
            `<div class="level-item support">${level.toFixed(5)}</div>`
        ).join('');
    }
    
    // Update trend information
    document.getElementById('primary-trend').textContent = structure.primaryTrend;
    document.getElementById('primary-trend').className = `trend-value ${structure.primaryTrend.toLowerCase()}`;
    document.getElementById('trend-strength-fill').style.width = structure.trendStrength + '%';
}

// Update trading setups
function updateTradingSetups(pyramidData, chartData) {
    const setups = generateTradingSetups(pyramidData, chartData);
    const container = document.getElementById('setup-cards');
    if (!container) return;
    
    if (setups.length === 0) {
        container.innerHTML = '<div class="no-setups">No high-probability setups detected</div>';
        return;
    }
    
    container.innerHTML = setups.map(setup => `
        <div class="setup-card ${setup.direction}">
            <div class="setup-header">
                <span class="setup-type">${setup.type}</span>
                <span class="setup-confidence ${getConfidenceClass(setup.confidence)}">
                    ${setup.confidence}%
                </span>
            </div>
            <div class="setup-details">
                <div class="setup-direction ${setup.direction}">${setup.direction.toUpperCase()}</div>
                <div class="setup-metrics">
                    <div class="setup-metric">
                        <span>R:R</span>
                        <span>${setup.riskReward}</span>
                    </div>
                    <div class="setup-metric">
                        <span>Stop Loss</span>
                        <span>${setup.stopLoss}</span>
                    </div>
                    <div class="setup-metric">
                        <span>Target</span>
                        <span>${setup.target}</span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Update volume analysis
function updateVolumeAnalysis(pyramidData) {
    const volumeAnalysis = analyzeVolume(pyramidData);
    
    // Update volume metrics
    document.getElementById('volume-trend').textContent = volumeAnalysis.trend;
    document.getElementById('volume-trend').className = `volume-value ${volumeAnalysis.trend.toLowerCase()}`;
    
    document.getElementById('volume-vs-avg').textContent = volumeAnalysis.vsAverage;
    document.getElementById('volume-confirmation').textContent = volumeAnalysis.confirmation;
    document.getElementById('volume-confirmation').className = `volume-value ${volumeAnalysis.confirmation.toLowerCase()}`;
    
    // Update volume bars
    document.getElementById('volume-d1').style.height = volumeAnalysis.timeframes.D1 + '%';
    document.getElementById('volume-h4').style.height = volumeAnalysis.timeframes.H4 + '%';
    document.getElementById('volume-h1').style.height = volumeAnalysis.timeframes.H1 + '%';
    document.getElementById('volume-m15').style.height = volumeAnalysis.timeframes.M15 + '%';
}

// ==================== ANALYSIS CALCULATIONS ====================

// Calculate timeframe strength
function calculateTimeframeStrength(block) {
    // Simple strength calculation based on momentum summary
    let strength = 0.5; // Default neutral
    
    if (block.momentum_summary) {
        if (block.momentum_summary.includes('Strong')) strength = 0.8;
        else if (block.momentum_summary.includes('Weak')) strength = 0.3;
        
        if (block.dir === '🟢') strength += 0.1;
        else if (block.dir === '🔴') strength -= 0.1;
    }
    
    return Math.max(0, Math.min(1, strength));
}

// Calculate indicator consensus
function calculateIndicatorConsensus(pyramidData) {
    // Simplified consensus calculation
    return {
        trend: Math.round(70 + Math.random() * 20), // Would use real indicator data
        momentum: Math.round(60 + Math.random() * 30),
        volatility: Math.round(50 + Math.random() * 40)
    };
}

// Analyze market structure (placeholder - would use real chart data)
function analyzeMarketStructure(chartData) {
    return {
        resistanceLevels: [1.0950, 1.0975, 1.1000],
        supportLevels: [1.0900, 1.0880, 1.0850],
        primaryTrend: 'Bullish',
        trendStrength: 75
    };
}

// Generate trading setups (placeholder)
function generateTradingSetups(pyramidData, chartData) {
    const setups = [];
    
    // Example setup
    if (gaugeValues.momentum > 70) {
        setups.push({
            type: 'Momentum Breakout',
            direction: 'long',
            confidence: 75,
            riskReward: '1:2.5',
            stopLoss: '1.0880',
            target: '1.1020'
        });
    }
    
    return setups;
}

// Analyze volume (placeholder)
function analyzeVolume(pyramidData) {
    return {
        trend: 'Increasing',
        vsAverage: '+25%',
        confirmation: 'Strong',
        timeframes: {
            D1: 80,
            H4: 65,
            H1: 45,
            M15: 30
        }
    };
}

// ==================== ENHANCED ANALYSIS DISPLAY ====================

// Update analysis data with confluence calculation
function updateAnalysis(data) {
    if (!data) return;
    
    currentAnalysis = data;
    
    // Calculate confluence if we have pyramid data
    if (data.blocks) {
        calculateConfluence(data);
        updateEnhancedAnalysis(data, {});
    }
    
    renderTechnicalSummary(data);
    renderTradingSignals(data);
    renderMarketStructure(data);
    
    // Check for alerts based on confluence
    checkConfluenceAlerts();
}

// Enhanced technical summary with confluence
function renderTechnicalSummary(data) {
    const summaryElement = document.getElementById('technicalSummary');
    if (!summaryElement) return;
    
    if (data.error) {
        summaryElement.innerHTML = `<div class="error">${data.error}</div>`;
        return;
    }
    
    const momentumText = getMomentumText(gaugeValues.momentum);
    const strengthText = getStrengthText(gaugeValues.strength);
    const riskText = getRiskText(gaugeValues.risk);
    
    summaryElement.innerHTML = `
        <div class="summary-content">
            <div class="summary-item">
                <span class="label">Market Confluence:</span>
                <span class="value ${getMomentumClass(gaugeValues.momentum)}">${momentumText}</span>
            </div>
            <div class="summary-item">
                <span class="label">Trend Strength:</span>
                <span class="value ${getStrengthClass(gaugeValues.strength)}">${strengthText}</span>
            </div>
            <div class="summary-item">
                <span class="label">Risk Level:</span>
                <span class="value ${getRiskClass(gaugeValues.risk)}">${riskText}</span>
            </div>
            ${data.technical_summary ? `
            <div class="summary-item">
                <span class="label">Latest Signal:</span>
                <span class="value">${data.technical_summary}</span>
            </div>
            ` : ''}
        </div>
    `;
}

// Render trading signals
function renderTradingSignals(data) {
    const signalsElement = document.getElementById('tradingSignals');
    if (!signalsElement) return;
    
    if (data.error || !data.trading_signals) {
        signalsElement.innerHTML = '<div class="no-signals">No signals available</div>';
        return;
    }
    
    let signalsHTML = '';
    data.trading_signals.forEach((signal, index) => {
        const signalType = getSignalType(signal);
        signalsHTML += `
            <div class="signal-item ${signalType}">
                <div class="signal-icon">${getSignalIcon(signalType)}</div>
                <div class="signal-content">
                    <div class="signal-text">${signal}</div>
                    <div class="signal-meta">${new Date().toLocaleTimeString()}</div>
                </div>
            </div>
        `;
    });
    
    signalsElement.innerHTML = signalsHTML || '<div class="no-signals">No active signals</div>';
}

// Render market structure
function renderMarketStructure(data) {
    const structureElement = document.getElementById('marketStructure');
    if (!structureElement) return;
    
    if (data.error || !data.market_structure) {
        structureElement.innerHTML = '<div class="no-data">Market structure data unavailable</div>';
        return;
    }
    
    structureElement.innerHTML = `
        <div class="structure-content">
            <div class="structure-item">
                <span class="label">Timeframe Analysis:</span>
                <span class="value">${data.market_structure}</span>
            </div>
        </div>
    `;
}

// ==================== ALERT SYSTEM ENHANCEMENTS ====================

// Check for confluence-based alerts
function checkConfluenceAlerts() {
    if (!alertSettings.momentumAlerts) return;
    
    // High momentum alert
    if (gaugeValues.momentum >= 80) {
        createAlert('momentum', `Strong bullish confluence detected (${gaugeValues.momentum}%)`, 'high');
    } else if (gaugeValues.momentum <= 20) {
        createAlert('momentum', `Strong bearish confluence detected (${gaugeValues.momentum}%)`, 'high');
    }
    
    // High volatility alert
    if (gaugeValues.volatility >= 80) {
        createAlert('volatility', `High market volatility detected (${gaugeValues.volatility}%)`, 'medium');
    }
    
    // High risk alert
    if (gaugeValues.risk >= 80) {
        createAlert('risk', `Elevated market risk level (${gaugeValues.risk}%)`, 'high');
    }
}

// ==================== ALERT MANAGEMENT ====================

// Toggle alert setting
function toggleAlertSetting(setting, enabled) {
    alertSettings[setting] = enabled;
    saveAlertSettings();
    console.log(`Alert setting ${setting} ${enabled ? 'enabled' : 'disabled'}`);
}

// Create new alert
function createAlert(type, message, priority = 'medium') {
    const alert = {
        id: generateAlertId(),
        type: type,
        message: message,
        priority: priority,
        time: new Date().toLocaleTimeString(),
        resolved: false
    };
    
    activeAlerts.unshift(alert); // Add to beginning
    if (activeAlerts.length > 50) {
        activeAlerts.pop(); // Keep only last 50 alerts
    }
    
    renderActiveAlerts();
    showAlertNotification(alert);
    
    return alert;
}

// Resolve alert
function resolveAlert(alertId) {
    const alert = activeAlerts.find(a => a.id === alertId);
    if (alert) {
        alert.resolved = true;
        alert.resolvedTime = new Date().toLocaleTimeString();
        renderActiveAlerts();
    }
}

// Clear all alerts
function clearAllAlerts() {
    activeAlerts = [];
    renderActiveAlerts();
}

// Test alert system
function testAlertSystem() {
    createAlert('test', 'This is a test alert - system is working correctly', 'low');
}

// ==================== ALERT CHECKING ====================

// Check for RSI alerts
function checkRSIAlerts(rsiValue) {
    if (!alertSettings.rsiAlerts) return;
    
    if (rsiValue > 70) {
        createAlert('rsi', `RSI Overbought: ${rsiValue.toFixed(1)} - Potential sell signal`, 'high');
    } else if (rsiValue < 30) {
        createAlert('rsi', `RSI Oversold: ${rsiValue.toFixed(1)} - Potential buy signal`, 'high');
    }
}

// Check for price alerts (placeholder)
function checkPriceAlerts(currentPrice, symbol) {
    if (!alertSettings.priceAlerts) return;
    // Implementation would track key price levels
}

// Check for volume alerts (placeholder)
function checkVolumeAlerts(currentVolume, averageVolume) {
    if (!alertSettings.volumeAlerts) return;
    
    if (currentVolume > averageVolume * 2) {
        createAlert('volume', `Volume spike detected: ${(currentVolume/averageVolume).toFixed(1)}x average`, 'medium');
    }
}

// ==================== ALERT RENDERING ====================

// Render alerts sections
function renderAlertsSections() {
    renderActiveAlerts();
    renderAlertSettings();
}

// Render active alerts
function renderActiveAlerts() {
    const alertsElement = document.getElementById('activeAlerts');
    if (!alertsElement) return;
    
    if (activeAlerts.length === 0) {
        alertsElement.innerHTML = `
            <div class="no-alerts">
                <div class="no-alerts-icon">🔕</div>
                <div class="no-alerts-text">No active alerts</div>
                <div class="no-alerts-subtext">Alerts will appear here when triggered</div>
            </div>
        `;
        return;
    }
    
    let alertsHTML = '';
    activeAlerts.forEach(alert => {
        alertsHTML += `
            <div class="alert-item ${alert.resolved ? 'resolved' : 'active'} ${alert.type}">
                <div class="alert-header">
                    <span class="alert-type">${alert.type}</span>
                    <span class="alert-time">${alert.time}</span>
                </div>
                <div class="alert-message">${alert.message}</div>
                ${!alert.resolved ? `
                    <div class="alert-actions">
                        <button class="alert-btn resolve" onclick="resolveAlert('${alert.id}')">
                            Mark Resolved
                        </button>
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    alertsElement.innerHTML = alertsHTML;
}

// Render alert settings
function renderAlertSettings() {
    const settingsElement = document.getElementById('alertSettings');
    if (!settingsElement) return;
    
    settingsElement.innerHTML = `
        <div class="alert-setting-group">
            <div class="alert-setting-item">
                <input type="checkbox" id="rsiAlert" ${alertSettings.rsiAlerts ? 'checked' : ''} 
                       onchange="toggleAlertSetting('rsiAlerts', this.checked)">
                <label for="rsiAlert">RSI Overbought/Oversold (70/30)</label>
            </div>
            <div class="alert-setting-item">
                <input type="checkbox" id="priceAlert" ${alertSettings.priceAlerts ? 'checked' : ''}
                       onchange="toggleAlertSetting('priceAlerts', this.checked)">
                <label for="priceAlert">Key Price Level Breaks</label>
            </div>
            <div class="alert-setting-item">
                <input type="checkbox" id="volumeAlert" ${alertSettings.volumeAlerts ? 'checked' : ''}
                       onchange="toggleAlertSetting('volumeAlerts', this.checked)">
                <label for="volumeAlert">Volume Spikes (2x Average)</label>
            </div>
            <div class="alert-setting-item">
                <input type="checkbox" id="momentumAlert" ${alertSettings.momentumAlerts ? 'checked' : ''}
                       onchange="toggleAlertSetting('momentumAlerts', this.checked)">
                <label for="momentumAlert">Momentum Shifts</label>
            </div>
        </div>
        <div class="alert-actions-global">
            <button class="alert-btn test" onclick="testAlertSystem()">Test Alert System</button>
            <button class="alert-btn clear" onclick="clearAllAlerts()">Clear All Alerts</button>
        </div>
    `;
}

// ==================== UTILITY FUNCTIONS ====================

// Get signal type from signal text
function getSignalType(signal) {
    if (signal.toLowerCase().includes('buy') || signal.toLowerCase().includes('bullish')) {
        return 'bullish';
    } else if (signal.toLowerCase().includes('sell') || signal.toLowerCase().includes('bearish')) {
        return 'bearish';
    }
    return 'neutral';
}

// Get signal icon
function getSignalIcon(signalType) {
    switch(signalType) {
        case 'bullish': return '🟢';
        case 'bearish': return '🔴';
        default: return '⚪';
    }
}

// Get momentum description text
function getMomentumText(value) {
    if (value >= 80) return 'Very Bullish';
    if (value >= 67) return 'Bullish';
    if (value >= 45) return 'Slightly Bullish';
    if (value >= 33) return 'Neutral';
    if (value >= 20) return 'Slightly Bearish';
    if (value >= 0) return 'Bearish';
    return 'Very Bearish';
}

// Get strength description text
function getStrengthText(value) {
    if (value >= 80) return 'Very Strong';
    if (value >= 67) return 'Strong';
    if (value >= 45) return 'Moderate';
    if (value >= 33) return 'Weak';
    return 'Very Weak';
}

// Get risk description text
function getRiskText(value) {
    if (value >= 80) return 'Very High';
    if (value >= 67) return 'High';
    if (value >= 45) return 'Medium';
    if (value >= 33) return 'Low';
    return 'Very Low';
}

// Get CSS classes for values
function getMomentumClass(value) {
    if (value >= 67) return 'bullish';
    if (value <= 33) return 'bearish';
    return 'neutral';
}

function getStrengthClass(value) {
    if (value >= 67) return 'strong';
    if (value <= 33) return 'weak';
    return 'moderate';
}

function getRiskClass(value) {
    if (value >= 67) return 'high';
    if (value <= 33) return 'low';
    return 'medium';
}

function getConsensusClass(percent) {
    if (percent >= 80) return 'strong';
    if (percent >= 60) return 'moderate';
    return 'weak';
}

function getConsensusText(percent) {
    if (percent >= 80) return 'Strong Agreement';
    if (percent >= 60) return 'Moderate Agreement';
    return 'Weak Agreement';
}

function getConfidenceClass(confidence) {
    if (confidence >= 80) return 'high';
    if (confidence >= 60) return 'medium';
    return 'low';
}

// Generate unique alert ID
function generateAlertId() {
    return 'alert_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Show alert notification
function showAlertNotification(alert) {
    // Could integrate with browser notifications here
    console.log(`ALERT: ${alert.type} - ${alert.message}`);
}

// Load alert settings from localStorage
function loadAlertSettings() {
    try {
        const saved = localStorage.getItem('megaFlowz_alertSettings');
        if (saved) {
            alertSettings = { ...alertSettings, ...JSON.parse(saved) };
        }
    } catch (e) {
        console.warn('Could not load alert settings:', e);
    }
}

// Save alert settings to localStorage
function saveAlertSettings() {
    try {
        localStorage.setItem('megaFlowz_alertSettings', JSON.stringify(alertSettings));
    } catch (e) {
        console.warn('Could not save alert settings:', e);
    }
}

// Export functions for global access
window.analysisAlerts = {
    initialize: initializeAnalysisAlerts,
    updateAnalysis: updateAnalysis,
    calculateConfluence: calculateConfluence,
    createAlert: createAlert,
    resolveAlert: resolveAlert,
    clearAllAlerts: clearAllAlerts,
    checkRSIAlerts: checkRSIAlerts,
    checkPriceAlerts: checkPriceAlerts,
    checkVolumeAlerts: checkVolumeAlerts
};

// Make functions globally available
window.toggleAlert = toggleAlertSetting;
window.resolveAlert = resolveAlert;
window.clearAllAlerts = clearAllAlerts;
window.testAlertSystem = testAlertSystem;