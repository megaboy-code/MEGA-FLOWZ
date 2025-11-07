// ===============================================================
// ⚡ MEGA FLOWZ DASHBOARD - REORGANIZED SCRIPT
// ===============================================================

// ==================== GLOBAL STATE & CONFIG ====================

// Global state
let currentChart = null;
let currentChartType = 'line';
let currentTimeframe = 'H1';
let currentPyramidStyle = 'daily';
let currentPair = 'EUR/USD';
let activeIndicators = new Map();
let crosshairEnabled = true;

// Smart Polling System State
let isActivePollingMode = false;
let activePollingTimer = null;
let pollingInterval = null;
const ACTIVE_POLL_INTERVAL = 2000;    // 2 seconds during active mode
const NORMAL_POLL_INTERVAL = 30000;   // 30 seconds during normal mode
const ACTIVE_POLL_DURATION = 10000;   // 10 seconds active window
let activePollCount = 0;
const MAX_ACTIVE_POLLS = 5;           // Maximum 5 polls during active mode

// Loading states
let isLoadingNewPair = false;
let currentLiveIcon = null;
let lastDataUpdateTime = null;
let isBackendOnline = true;

// Chart colors
let chartColors = {
    line: '#3A86FF',
    areaFill: 'rgba(58, 134, 255, 0.15)',
    bull: '#00D394',
    bear: '#EF4444'
};

// Real-time axis indicators
let axisIndicators = {
    yIndicator: null,
    xIndicator: null
};

// Crosshair state
let crosshairVisible = false;
let crosshairX = 0;
let crosshairY = 0;
let crosshairPrice = null;

// Tooltip locking variables
let tooltipLocked = false;
let lockedTooltipPosition = null;

// Track pyramid block for tooltip positioning
let lastClickedPyramidBlock = null;

// Pyramid style configurations
const pyramidStructures = {
    'scalper': ['M15', 'M5', 'M1'],
    'intraday': ['H1', 'M15', 'M5', 'M1'],
    'swing': ['H4', 'H1', 'M15', 'M5', 'M1'],
    'daily': ['D1', 'H4', 'H1', 'M15', 'M5', 'M1']
};

const pyramidStyleNames = {
    'scalper': '⚡ Scalper',
    'intraday': '📈 Intraday', 
    'swing': '🔄 Swing',
    'daily': '📅 Daily'
};

let timeframeVisibility = {
    'D1': true, 'H4': true, 'H1': true, 
    'M15': true, 'M5': true, 'M1': true
};

// Expected child counts for progress calculation
const expectedChildCounts = {
    'D1': 6,   // 6 H4 blocks in a day
    'H4': 4,   // 4 H1 blocks in 4 hours
    'H1': 4,   // 4 M15 blocks in 1 hour
    'M15': 3,  // 3 M5 blocks in 15 minutes
    'M5': 5    // 5 M1 blocks in 5 minutes
};

// Indicator management
let indicatorInstances = {
    sma: [], ema: [], rsi: [], macd: [], bollinger: [], stochastic: [], supportresistance: []
};

// Track real indicator values from backend
let currentIndicatorValues = {};

// DOM elements
const status = document.getElementById('status');
const updateInfo = document.getElementById('updateInfo');
const pyramidDiv = document.getElementById('pyramid');
const expandedBlocks = new Set();

// ==================== INITIALIZATION ====================

function initializeDashboard() {
    console.log("🧠 Initializing MEGA FLOWZ Professional Dashboard...");
    
    // Set defaults
    const pairsSelect = document.getElementById('pairsSelect');
    if (pairsSelect) pairsSelect.value = 'EUR/USD';
    
    // UPDATE: Add candlestick option to dropdown
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.innerHTML = `
            <option value="line">📈 Line</option>
            <option value="area">🟦 Area</option>
            <option value="candlestick">🕯️ Candlestick</option>
            <option value="trend">🎯 Bull/Bear Trend</option>
        `;
        chartTypeSelect.value = 'line';
    }
    
    // Initialize smart polling system
    initializeSmartPolling();
    
    // Initialize components
    initializeIndicatorsPanel();
    initializeColorPickers();
    
    // Start backend status monitoring
    setInterval(checkBackendStatus, 5000);
    
    // Load initial data
    changePyramidStyle('daily');
    updateDashboard();
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);

    console.log("✅ Dashboard initialized successfully");
}

function checkBackendStatus() {
    if (!lastDataUpdateTime) return;
    
    const timeSinceLastUpdate = Date.now() - lastDataUpdateTime;
    const isOffline = timeSinceLastUpdate > 35000; // 35 seconds without data
    
    if (isOffline && isBackendOnline && currentLiveIcon) {
        console.log("🔴 Backend appears offline");
        isBackendOnline = false;
        currentLiveIcon.style.color = '#EF4444'; // Red for offline
        currentLiveIcon.classList.remove('pulsing');
        currentLiveIcon.classList.add('offline');
    }
}

// Start the dashboard when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboard);
} else {
    initializeDashboard();
}

console.log("🚀 MEGA FLOWZ Dashboard Script Loaded Successfully!");

// ==================== SMART POLLING SYSTEM ====================

function initializeSmartPolling() {
    console.log("🔄 Initializing Smart Polling System...");
    startPolling();
    setupUserActivityListeners();
}

function onUserAction(actionType = 'unknown') {
    console.log(`🎯 User action detected: ${actionType}`);
    
    // Only trigger active polling for pair and style changes
    if (actionType !== 'pair_change' && actionType !== 'pyramid_style_change') {
        console.log(`🔕 Skipping active polling for: ${actionType}`);
        return;
    }
    
    // Set active polling state
    isActivePollingMode = true;
    activePollCount = 0;
    
    // Clear existing timers
    if (activePollingTimer) {
        clearTimeout(activePollingTimer);
    }
    
    // Set timer to return to normal mode
    activePollingTimer = setTimeout(() => {
        console.log("🔄 Returning to normal polling mode (30s)");
        isActivePollingMode = false;
        activePollCount = 0;
        restartPolling();
    }, ACTIVE_POLL_DURATION);
    
    // Immediate data refresh
    updateDashboard();
    
    // Restart polling with active interval
    restartPolling();
}

function startPolling() {
    // Clear existing interval
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
    
    // Start new interval based on current mode
    const interval = isActivePollingMode ? ACTIVE_POLL_INTERVAL : NORMAL_POLL_INTERVAL;
    console.log(`📡 Starting ${isActivePollingMode ? 'ACTIVE' : 'NORMAL'} mode polling: ${interval/1000}s interval`);
    
    pollingInterval = setInterval(() => {
        if (isActivePollingMode) {
            activePollCount++;
            console.log(`🔍 Active poll #${activePollCount}`);
            
            // Stop active polling after max polls reached
            if (activePollCount >= MAX_ACTIVE_POLLS) {
                console.log("🔄 Max active polls reached, returning to normal mode");
                isActivePollingMode = false;
                activePollCount = 0;
                restartPolling();
                return;
            }
        }
        updateDashboard();
    }, interval);
}

function restartPolling() {
    console.log(`🔄 Restarting polling in ${isActivePollingMode ? 'ACTIVE' : 'NORMAL'} mode`);
    startPolling();
}

function setupUserActivityListeners() {
    // Pair dropdown change - KEEP THIS
    const pairsSelect = document.getElementById('pairsSelect');
    if (pairsSelect) {
        pairsSelect.addEventListener('change', (e) => {
            showReloadingSign();
            onUserAction('pair_change');
            changePair(e.target.value);
        });
    }
    
    // Pyramid style dropdown change - KEEP THIS
    const pyramidStyleSelect = document.getElementById('pyramidStyleSelect');
    if (pyramidStyleSelect) {
        pyramidStyleSelect.addEventListener('change', (e) => {
            showReloadingSign();
            onUserAction('pyramid_style_change');
            changePyramidStyle(e.target.value);
        });
    }
    
    // REMOVED: Chart interactions - no longer trigger active polling
    const chartCanvas = document.getElementById('mainChart');
    if (chartCanvas) {
        // Keep functionality but don't trigger active polling
        chartCanvas.addEventListener('click', () => {
            // Chart click functionality without active polling
        });
        chartCanvas.addEventListener('mousemove', () => {
            // Chart hover functionality without active polling
        });
    }
    
    // REMOVED: Indicator interactions - no longer trigger active polling
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('indicator-btn') || 
            e.target.classList.contains('setting-group') ||
            e.target.closest('.indicator-settings')) {
            // Indicator adjustments without active polling
        }
    });
    
    // REMOVED: Pyramid size buttons - no longer trigger active polling
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('size-btn')) {
            // Pyramid size changes without active polling
        }
    });
    
    // REMOVED: Timeframe changes - no longer trigger active polling
    const timeframeSelect = document.getElementById('timeframeSelect');
    if (timeframeSelect) {
        timeframeSelect.addEventListener('change', () => {
            // Timeframe changes without active polling
            loadChart(timeframeSelect.value);
        });
    }
    
    // REMOVED: Chart type changes - no longer trigger active polling
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.addEventListener('change', () => {
            // Chart type changes without active polling
            setChartType(chartTypeSelect.value);
        });
    }
    
    console.log("✅ User activity listeners setup complete");
}

function getPollingStatus() {
    return {
        isActivePollingMode: isActivePollingMode,
        currentInterval: isActivePollingMode ? ACTIVE_POLL_INTERVAL : NORMAL_POLL_INTERVAL,
        mode: isActivePollingMode ? 'ACTIVE' : 'NORMAL',
        activePollCount: activePollCount,
        maxActivePolls: MAX_ACTIVE_POLLS,
        timeUntilNormal: activePollingTimer ? 'active' : 'normal'
    };
}

// ==================== LOADING STATES MANAGEMENT ====================

function showReloadingSign() {
    // Remove existing live icon
    if (currentLiveIcon) {
        currentLiveIcon.remove();
        currentLiveIcon = null;
    }
    
    // Create or update reloading sign
    let reloadingSign = document.getElementById('reloadingSign');
    if (!reloadingSign) {
        reloadingSign = document.createElement('div');
        reloadingSign.id = 'reloadingSign';
        reloadingSign.className = 'reloading-sign';
        reloadingSign.innerHTML = '🔄 Loading...';
        
        const header = document.querySelector('.header');
        if (header) {
            header.appendChild(reloadingSign);
        }
    }
    
    reloadingSign.style.display = 'block';
    isLoadingNewPair = true;
}

function hideReloadingSign() {
    const reloadingSign = document.getElementById('reloadingSign');
    if (reloadingSign) {
        reloadingSign.style.display = 'none';
    }
    isLoadingNewPair = false;
}

function showLiveIcon() {
    // Hide reloading sign first
    hideReloadingSign();
    
    // Update last data update time
    lastDataUpdateTime = Date.now();
    isBackendOnline = true;
    
    // Create small live pulsing icon
    if (!currentLiveIcon) {
        currentLiveIcon = document.createElement('div');
        currentLiveIcon.className = 'live-icon';
        currentLiveIcon.innerHTML = '●';
        currentLiveIcon.style.fontSize = '12px';
        currentLiveIcon.style.width = '16px';
        currentLiveIcon.style.height = '16px';
        currentLiveIcon.style.display = 'flex';
        currentLiveIcon.style.alignItems = 'center';
        currentLiveIcon.style.justifyContent = 'center';
        
        const header = document.querySelector('.header');
        if (header) {
            header.appendChild(currentLiveIcon);
        }
        
        // Add pulsing animation
        setTimeout(() => {
            if (currentLiveIcon) {
                currentLiveIcon.classList.add('pulsing');
                currentLiveIcon.style.color = '#00D394'; // Green for online
            }
        }, 100);
    } else {
        // Update existing icon to online state
        currentLiveIcon.style.color = '#00D394';
        currentLiveIcon.classList.add('pulsing');
        currentLiveIcon.classList.remove('offline');
    }
}

// ==================== PYRAMID FUNCTIONS ====================

function setPyramidSize(size) {
    document.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    pyramidDiv.className = 'pyramid ' + size;
}

function getBlockId(block) { return `${block.tf}_${block.time}`; }

function shouldDisplayBlock(block) {
    if (!timeframeVisibility[block.tf]) return false;
    if (block.children && block.children.length > 0) {
        return block.children.some(child => shouldDisplayBlock(child));
    }
    return true;
}

// UPDATED: Calculate pips with crypto detection
function calculatePips(block) {
    if (!block.H || !block.L) return 0;
    
    const high = parseFloat(block.H);
    const low = parseFloat(block.L);
    const range = high - low;
    
    // Detect pair type and apply correct pip calculation
    if (currentPair.includes('JPY')) {
        // JPY pairs: 2-3 decimal places, pip = 0.01
        return Math.round(range * 100) + "pips";
    } else if (currentPair.includes('BTC') || currentPair.includes('ETH') || currentPair.includes('XRP') || 
               currentPair.includes('ADA') || currentPair.includes('DOT') || currentPair.includes('LTC')) {
        // Crypto pairs: use points (raw price difference)
        return Math.round(range) + "points";
    } else {
        // Most forex pairs: 4-5 decimal places, pip = 0.0001
        return Math.round(range * 10000) + "pips";
    }
}

// UPDATED: Calculate completion progress with fixed expected totals and color coding
function calculateProgress(block) {
    if (!block.children || block.children.length === 0) {
        return { hasProgress: false };
    }
    
    // Get expected total for this timeframe
    const expectedTotal = expectedChildCounts[block.tf] || block.children.length;
    
    // FIXED: Count completed children (ALL blocks with momentum, including neutral)
    const completed = block.children.filter(child => 
        child.momentum_summary  // ← Only check for momentum data, include neutral blocks
    ).length;
    
    // Determine status for color coding
    let status = '';
    if (completed === expectedTotal) {
        status = 'complete'; // Green - fully complete
    } else if (completed > 0) {
        status = 'partial';  // Blue - partially complete
    }
    // No status if completed === 0
    
    return {
        hasProgress: expectedTotal > 0,
        completed: completed,
        total: expectedTotal, // Use fixed expected total, not visible count
        status: status
    };
}

// UPDATED: Create block with corrected pips, progress, and color coding
function createBlock(block, level = 0) {
    if (!shouldDisplayBlock(block)) return null;

    const blockId = getBlockId(block);
    const div = document.createElement('div');
    div.className = `block ${block.dir === '🟢' ? 'green' : block.dir === '🔴' ? 'red' : 'gray'}`;
    div.dataset.id = blockId;

    const isExpanded = expandedBlocks.has(blockId);
    const hasChildren = block.children && block.children.some(child => shouldDisplayBlock(child));
    
    // UPDATED: Calculate pips and progress with corrected logic
    const pips = calculatePips(block);
    const progressInfo = calculateProgress(block);

    // UPDATED: Include corrected pips and progress with color coding
    div.innerHTML = `
        <div class="header-line">
            <span class="toggle" onclick="toggleBlock('${blockId}', this)">
                ${hasChildren ? (isExpanded ? '📂' : '📁') : '📄'} 
                ${block.tf} ${block.range} ${block.dir}
            </span>
            <span class="block-metrics">
                <span class="pips-value">${pips}</span>
                ${progressInfo.hasProgress ? `
                    <span class="progress-indicator ${progressInfo.status}">
                        ${progressInfo.completed}/${progressInfo.total}
                    </span>
                ` : ''}
            </span>
            <span class="ohlc">O:${block.O} H:${block.H} L:${block.L} C:${block.C} V:${formatVolume(block.volume)}</span>
        </div>
        <div class="momentum-summary">${block.momentum_summary}</div>
    `;

    if (hasChildren) {
        const children = document.createElement('div');
        children.className = `children ${isExpanded ? '' : 'hidden'}`;
        children.id = `children-${blockId}`;
        
        block.children.forEach(child => {
            const childElement = createBlock(child, level + 1);
            if (childElement) children.appendChild(childElement);
        });
        
        if (children.children.length > 0) div.appendChild(children);
    }
    
    div.addEventListener('click', function(e) {
        e.stopPropagation();
        
        if (!e.target.classList.contains('toggle')) {
            lastClickedPyramidBlock = block;
            switchToChartWithTimeframe(block);
        }
    });
    
    return div;
}

window.toggleBlock = function(blockId, element) {
    const children = document.getElementById(`children-${blockId}`);
    if (!children) return;

    const willExpand = children.classList.contains('hidden');
    children.classList.toggle('hidden');

    const icon = element.querySelector('span') || element;
    icon.innerHTML = willExpand ? icon.innerHTML.replace('📁', '📂') : icon.innerHTML.replace('📂', '📁');
    
    if (willExpand) expandedBlocks.add(blockId);
    else expandedBlocks.delete(blockId);
};

function switchToChartWithTimeframe(block) {
    switchTab('chart');
    
    setTimeout(() => {
        const timeframeSelect = document.getElementById('timeframeSelect');
        if (timeframeSelect) {
            timeframeSelect.value = block.tf;
            loadChart(block.tf);
        }
    }, 150);
}

// UPDATED: Render function with better loading states
function render(data) {
    const scrollPos = window.scrollY;
    pyramidDiv.innerHTML = '';
    
    if (!data || !data.blocks) {
        pyramidDiv.innerHTML = '<div class="loading">📊 Loading pyramid data...</div>';
        return;
    }

    if (status) status.textContent = `${currentPair} • ${pyramidStyleNames[currentPyramidStyle]}`;
    if (updateInfo) updateInfo.textContent = `Last Updated: ${new Date().toLocaleString()}`;
    
    let visibleBlocksCount = 0;
    data.blocks.forEach(block => {
        const blockElement = createBlock(block);
        if (blockElement) {
            pyramidDiv.appendChild(blockElement);
            visibleBlocksCount++;
        }
    });

    if (visibleBlocksCount === 0) {
        pyramidDiv.innerHTML = '<div class="loading">📊 Loading market data...</div>';
    } else {
        // Show live icon when data is successfully loaded
        showLiveIcon();
    }

    window.scrollTo(0, scrollPos);
}

// UPDATED: Better error handling in updateDashboard
function updateDashboard() {
    fetch(`/api/pyramid?pair=${currentPair}&pyramid_style=${currentPyramidStyle}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(render)
        .catch(error => {
            console.error('Dashboard update error:', error);
            if (status) status.textContent = '🔄 Updating market data...';
            if (updateInfo) updateInfo.textContent = 'Connecting to data source...';
            
            // Keep existing blocks visible during errors
            if (pyramidDiv.children.length === 0) {
                pyramidDiv.innerHTML = '<div class="loading">📊 Connecting to market data...</div>';
            }
        })
        .finally(() => {
            // Always hide reloading sign after attempt
            hideReloadingSign();
        });
}

function changePyramidStyle(style) {
    currentPyramidStyle = style;
    
    const selectedStructure = pyramidStructures[style];
    Object.keys(timeframeVisibility).forEach(tf => {
        timeframeVisibility[tf] = selectedStructure.includes(tf);
    });
    
    const dropdown = document.getElementById('pyramidStyleSelect');
    if (dropdown) dropdown.value = style;
    
    updateBackendSettings();
    updateDashboard();
}

function updateBackendSettings() {
    const settings = {
        symbol: currentPair.replace('/', ''),
        pyramid_style: currentPyramidStyle
    };
    
    fetch('/api/update-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('✅ Backend settings updated:', data.message);
        } else {
            console.error('❌ Backend settings update failed:', data.error);
        }
    })
    .catch(error => {
        console.error('❌ Backend settings sync error:', error);
    });
}

// UPDATED: changePair with better loading states
function changePair(pair) {
    currentPair = pair;
    const pairsSelect = document.getElementById('pairsSelect');
    if (pairsSelect) pairsSelect.value = pair;
    
    updateBackendSettings();
    updateDashboard();
    
    if (currentTimeframe) {
        loadChart(currentTimeframe);
    }
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    
    const targetTab = document.getElementById(tabName + '-tab');
    if (targetTab) targetTab.classList.add('active');
    
    event.target.classList.add('active');
    
    if (tabName === 'chart') {
        setTimeout(() => {
            if (!currentChart) {
                loadChart(currentTimeframe);
            }
        }, 100);
    }
}



// ==================== CHART SYSTEM ====================
// Chart rendering and datasets
function renderProfessionalChart(chartData, timeframe, symbol, indicators, indicators_data) {
    const ctx = document.getElementById('mainChart').getContext('2d');
   
    if (currentChart) currentChart.destroy();
    currentIndicatorValues = indicators || {};
   
    const professionalTheme = {
        primary: chartColors.line,
        background: chartColors.areaFill,
        grid: '#1E293B',
        text: '#F1F5F9',
        textSecondary: '#94A3B8',
        accent: '#8B5CF6',
        axisBorder: '#334155'
    };
    let datasets = [];
    if (currentChartType === 'line') {
        datasets = createLineDataset(chartData, symbol, professionalTheme);
    } else if (currentChartType === 'area') {
        datasets = createAreaDataset(chartData, symbol, professionalTheme);
    } else if (currentChartType === 'candlestick') {
        datasets = createCandlestickDataset(chartData, symbol, professionalTheme);
    } else if (currentChartType === 'trend') {
        datasets = createLineDataset(chartData, symbol, professionalTheme);
    }
    datasets = datasets.concat(createIndicatorDatasets(indicators_data, professionalTheme));
    const chartType = currentChartType === 'candlestick' ? 'candlestick' : 'line';
   
    currentChart = new Chart(ctx, {
        type: chartType,
        data: { datasets: datasets },
        options: getEnhancedChartOptions(timeframe, professionalTheme)
    });
    initializeCurrentPriceLevel();
    initializeCrosshairDisplay();
    addCrosshairListeners();
    initializeChartScroll();
    renderIndicatorsList();
   
    const latestPrice = chartData.length > 0 ? chartData[chartData.length - 1].y : 0;
    updateCurrentPrice(latestPrice);
    updateCurrentPriceLevel(latestPrice, 'neutral');
   
    console.log(`✅ Chart rendered: ${symbol} ${timeframe} (${currentChartType})`);
}

function loadChart(timeframe = 'H1') {
    const chartStatus = document.getElementById('chartStatus');
    if (!chartStatus) return;
   
    chartStatus.textContent = '🔄 Loading...';
   
    const indicatorParams = buildIndicatorParameters();
   
    fetch(`/api/chart-data/${timeframe}?pair=${currentPair}&pyramid_style=${currentPyramidStyle}${indicatorParams}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.error) {
                chartStatus.textContent = `❌ ${data.error}`;
                return;
            }
           
            // Validate chart data before rendering
            if (!data.data || !Array.isArray(data.data) || data.data.length === 0) {
                chartStatus.textContent = '❌ No chart data received';
                return;
            }
           
            renderProfessionalChart(data.data, timeframe, currentPair, data.indicators, data.indicators_data);
            chartStatus.textContent = `✅ ${currentPair} ${timeframe}`;
            currentTimeframe = timeframe;
           
            if (lastClickedPyramidBlock) {
                setTimeout(() => {
                    triggerTooltipAtTime(lastClickedPyramidBlock.time);
                    lastClickedPyramidBlock = null;
                }, 500);
            }
        })
        .catch(error => {
            console.error('Chart loading error:', error);
            chartStatus.textContent = '❌ Failed to load chart data';
        });
}

function buildIndicatorParameters() {
    let params = '';
    activeIndicators.forEach((config, indicatorId) => {
        const baseType = indicatorId.split('_')[0];
       
        switch(baseType) {
            case 'sma': case 'ema': case 'rsi':
                params += `&${baseType}_period=${config.period}`;
                break;
            case 'macd':
                params += `&${baseType}_fast=${config.fastPeriod}&${baseType}_slow=${config.slowPeriod}&${baseType}_signal=${config.signalPeriod}`;
                break;
            case 'bollinger':
                params += `&${baseType}_period=${config.period}&${baseType}_std=${config.stdDev}`;
                break;
            case 'stochastic':
                params += `&${baseType}_k=${config.kPeriod}&${baseType}_k_smooth=${config.kSmooth}&${baseType}_d_smooth=${config.dSmooth}`;
                break;
        }
       
        params += `&${baseType}_instance=${config.instanceNumber}`;
    });
   
    return params;
}

// Chart dataset creators
function createCandlestickDataset(priceData, symbol, theme) {
    return [{
        label: `${symbol} Price`,
        data: priceData,
        borderColor: theme.primary,
        backgroundColor: 'transparent',
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 3,
        tension: 0.1,
        yAxisID: 'y',
        fill: false
    }];
}

function createLineDataset(priceData, symbol, theme) {
    if (currentChartType === 'trend') {
        return [{
            label: `${symbol} Price`, data: priceData,
            segment: { borderColor: (ctx) => {
                if (ctx.p0.parsed.y === ctx.p1.parsed.y) return theme.primary;
                return ctx.p1.parsed.y > ctx.p0.parsed.y ? chartColors.bull : chartColors.bear;
            }},
            borderWidth: 2, pointRadius: 0, pointHoverRadius: 3, tension: 0.1, yAxisID: 'y', fill: false
        }];
    } else {
        return [{
            label: `${symbol} Price`, data: priceData, borderColor: theme.primary, backgroundColor: 'transparent',
            borderWidth: 2, pointRadius: 0, pointHoverRadius: 3, tension: 0.1, yAxisID: 'y', fill: false
        }];
    }
}

function createAreaDataset(priceData, symbol, theme) {
    return [{
        label: `${symbol} Price`, data: priceData, borderColor: theme.primary, backgroundColor: theme.background,
        borderWidth: 2, pointRadius: 0, pointHoverRadius: 3, tension: 0.1, yAxisID: 'y',
        fill: { target: 'origin', above: theme.background }
    }];
}

function createIndicatorDatasets(indicators_data, theme) {
    const datasets = [];
    if (!indicators_data) return datasets;
   
    activeIndicators.forEach((config, indicatorId) => {
        if (!config.visible) return;
        const baseType = indicatorId.split('_')[0];
       
        switch(baseType) {
            case 'bollinger':
                if (indicators_data.bollinger) {
                    const bb = indicators_data.bollinger;
                    datasets.push(
                        { label: `${config.name} Upper`, data: bb.upper, borderColor: config.color, borderWidth: 1, pointRadius: 0, yAxisID: 'y', fill: false },
                        { label: `${config.name} Middle`, data: bb.middle, borderColor: config.color, borderWidth: 1.5, pointRadius: 0, yAxisID: 'y', fill: false },
                        { label: `${config.name} Lower`, data: bb.lower, borderColor: config.color, borderWidth: 1, pointRadius: 0, yAxisID: 'y', fill: false }
                    );
                }
                break;
            case 'stochastic':
                if (indicators_data.stoch_k) {
                    datasets.push({ label: `${config.name} %K`, data: indicators_data.stoch_k, borderColor: config.color, borderWidth: 1.5, pointRadius: 0, yAxisID: 'y2', fill: false });
                }
                if (indicators_data.stoch_d) {
                    datasets.push({ label: `${config.name} %D`, data: indicators_data.stoch_d, borderColor: config.color, borderWidth: 1.5, borderDash: [5, 5], pointRadius: 0, yAxisID: 'y2', fill: false });
                }
                break;
            case 'supportresistance':
                if (indicators_data.support_resistance) {
                    datasets.push({ label: 'Support/Resistance', data: [], srLevels: indicators_data.support_resistance, supportColor: config.supportColor, resistanceColor: config.resistanceColor });
                }
                break;
            default:
                const instanceNumber = config.instanceNumber;
                const dataKeys = [`${baseType}_${config.period}`, `${baseType}_${instanceNumber}`, baseType, `${baseType}_20`, `${baseType}_12`];
               
                let indicatorData = null;
                for (const key of dataKeys) {
                    if (indicators_data[key]) {
                        indicatorData = indicators_data[key];
                        break;
                    }
                }
               
                if (indicatorData) {
                    datasets.push({
                        label: `${config.name} #${instanceNumber}`, data: indicatorData, borderColor: config.color, borderWidth: 1.5,
                        borderDash: baseType === 'ema' ? [2, 2] : [0, 0], pointRadius: 0, tension: 0, yAxisID: config.yAxis || 'y', fill: false
                    });
                }
                break;
        }
    });
    return datasets;
}

// Chart options and configuration with better axis frames
function getEnhancedChartOptions(timeframe, theme) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'nearest',
            intersect: false,
            axis: 'xy'
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: false,
                mode: 'nearest',
                intersect: false,
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                titleColor: theme.text,
                bodyColor: theme.textSecondary,
                borderColor: theme.grid,
                borderWidth: 1,
                cornerRadius: 6,
                padding: 12,
                callbacks: {
                    title: function(context) {
                        const date = new Date(context[0].parsed.x);
                        return date.toLocaleDateString('en-US', {
                            weekday: 'short',
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                            hour12: false
                        });
                    },
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) label += ': ';
                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-US', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 5
                            }).format(context.parsed.y);
                        }
                        return label;
                    }
                }
            },
            zoom: {
                zoom: {
                    drag: {
                        enabled: false,
                        modifierKey: null
                    },
                    wheel: {
                        enabled: false
                    },
                    pinch: {
                        enabled: false
                    },
                    mode: 'xy'
                },
                pan: {
                    enabled: true,
                    mode: 'xy',
                    modifierKey: 'shift'
                },
                limits: {
                    x: { min: 'original', max: 'original' },
                    y: { min: 'original', max: 'original' }
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    displayFormats: getProfessionalTimeFormats(timeframe)
                },
                grid: {
                    color: theme.grid,
                    drawBorder: true,
                    border: {
                        color: theme.axisBorder,
                        width: 2
                    }
                },
                ticks: {
                    color: theme.text,
                    maxRotation: 0,
                    autoSkip: true,
                    maxTicksLimit: 8,
                    padding: 8,
                    font: {
                        size: 11,
                        weight: '500'
                    }
                },
                border: {
                    display: true,
                    color: theme.axisBorder,
                    width: 2
                }
            },
            y: {
                position: 'right',
                grid: {
                    color: theme.grid,
                    drawBorder: true,
                    border: {
                        color: theme.axisBorder,
                        width: 2
                    }
                },
                ticks: {
                    color: theme.text,
                    callback: (value) => value.toFixed(5),
                    maxTicksLimit: 10,
                    padding: 8,
                    font: {
                        size: 11,
                        weight: '500'
                    }
                },
                border: {
                    display: true,
                    color: theme.axisBorder,
                    width: 2
                }
            },
            y2: {
                type: 'linear',
                position: 'left',
                grid: { drawOnChartArea: false },
                ticks: {
                    color: theme.text,
                    callback: (value) => value.toFixed(2),
                    maxTicksLimit: 5,
                    padding: 8,
                    font: {
                        size: 11,
                        weight: '500'
                    }
                },
                border: {
                    display: true,
                    color: theme.axisBorder,
                    width: 2
                },
                min: 0,
                max: 100
            }
        }
    };
}

// Chart Scroll Control
function initializeChartScroll() {
    const canvas = document.getElementById('mainChart');
    if (!canvas) return;
    
    canvas.addEventListener('wheel', function(event) {
        if (!currentChart) return;
        
        event.preventDefault();
        
        // Only allow horizontal scrolling (left/right)
        const xScale = currentChart.scales.x;
        if (!xScale) return;
        
        const currentMin = xScale.min;
        const currentMax = xScale.max;
        const range = currentMax - currentMin;
        const scrollSpeed = range * 0.1; // 10% scroll per wheel tick
        
        if (event.deltaY > 0) {
            // Scroll right (forward in time)
            currentChart.options.scales.x.min = currentMin + scrollSpeed;
            currentChart.options.scales.x.max = currentMax + scrollSpeed;
        } else {
            // Scroll left (back in time)
            currentChart.options.scales.x.min = currentMin - scrollSpeed;
            currentChart.options.scales.x.max = currentMax - scrollSpeed;
        }
        
        currentChart.update('none');
    });
}

// Current Price Level System - FIXED
function initializeCurrentPriceLevel() {
    const chartWrapper = document.querySelector('.chart-wrapper');
    if (!chartWrapper) return;
   
    const existingLine = document.getElementById('currentPriceLevel');
    if (existingLine) existingLine.remove();
   
    const currentPriceLevel = document.createElement('div');
    currentPriceLevel.id = 'currentPriceLevel';
    currentPriceLevel.className = 'current-price-level';
    currentPriceLevel.style.display = 'none';
   
    chartWrapper.appendChild(currentPriceLevel);
}

function updateCurrentPriceLevel(price, direction) {
    const currentPriceLevel = document.getElementById('currentPriceLevel');
    if (!currentPriceLevel || !currentChart) return;
   
    const chartArea = currentChart.chartArea;
    if (!chartArea) return;
   
    const yScale = currentChart.scales.y;
    const pixel = yScale.getPixelForValue(price);
   
    if (pixel >= chartArea.top && pixel <= chartArea.bottom) {
        currentPriceLevel.style.display = 'block';
        currentPriceLevel.style.top = `${pixel}px`;
        currentPriceLevel.style.left = `${chartArea.left}px`;
        currentPriceLevel.style.width = `${chartArea.right - chartArea.left}px`;
        currentPriceLevel.style.height = '1px';
       
        // Set color based on direction
        if (direction === 'up') {
            currentPriceLevel.style.backgroundColor = chartColors.bull;
            currentPriceLevel.classList.add('bull');
            currentPriceLevel.classList.remove('bear', 'neutral');
        } else if (direction === 'down') {
            currentPriceLevel.style.backgroundColor = chartColors.bear;
            currentPriceLevel.classList.add('bear');
            currentPriceLevel.classList.remove('bull', 'neutral');
        } else {
            currentPriceLevel.style.backgroundColor = chartColors.line;
            currentPriceLevel.classList.add('neutral');
            currentPriceLevel.classList.remove('bull', 'bear');
        }
       
        // Update Y-axis price box
        updateYAxisPriceBox(price, direction);
    } else {
        currentPriceLevel.style.display = 'none';
    }
}

function updateYAxisPriceBox(price, direction) {
    const chartWrapper = document.querySelector('.chart-wrapper');
    if (!chartWrapper) return;
   
    let priceBox = document.getElementById('yAxisPriceBox');
    if (!priceBox) {
        priceBox = document.createElement('div');
        priceBox.id = 'yAxisPriceBox';
        priceBox.className = 'y-axis-price-box';
        chartWrapper.appendChild(priceBox);
    }
   
    priceBox.textContent = price.toFixed(5);
    priceBox.style.display = 'block';
   
    // Position on Y-axis
    const chartArea = currentChart.chartArea;
    const yScale = currentChart.scales.y;
    const pixel = yScale.getPixelForValue(price);
   
    priceBox.style.top = `${pixel - 10}px`;
    priceBox.style.right = '0px';
   
    // Set color based on direction
    if (direction === 'up') {
        priceBox.style.backgroundColor = chartColors.bull;
        priceBox.style.color = '#000';
    } else if (direction === 'down') {
        priceBox.style.backgroundColor = chartColors.bear;
        priceBox.style.color = '#FFF';
    } else {
        priceBox.style.backgroundColor = chartColors.line;
        priceBox.style.color = '#FFF';
    }
}

// Enhanced Zoom System with Active State - FIXED
let isZoomModeActive = false;
let currentZoomMode = null;
let currentZoomLevel = 2;

function zoomIn() {
    if (!currentChart) return;
   
    // Toggle active state
    if (isZoomModeActive && currentZoomMode === 'in') {
        // Deactivate
        isZoomModeActive = false;
        currentZoomMode = null;
        currentChart.options.plugins.zoom.zoom.drag.enabled = false;
        updateZoomButtonState('reset');
    } else {
        // Activate
        isZoomModeActive = true;
        currentZoomMode = 'in';
        currentChart.options.plugins.zoom.zoom.drag.enabled = true;
        updateZoomButtonState('in');
    }
   
    currentChart.update('none');
}

function zoomOut() {
    if (!currentChart) return;
   
    // Toggle active state
    if (isZoomModeActive && currentZoomMode === 'out') {
        // Deactivate
        isZoomModeActive = false;
        currentZoomMode = null;
        currentChart.options.plugins.zoom.zoom.drag.enabled = false;
        updateZoomButtonState('reset');
    } else {
        // Activate
        isZoomModeActive = true;
        currentZoomMode = 'out';
        currentChart.options.plugins.zoom.zoom.drag.enabled = true;
        updateZoomButtonState('out');
    }
   
    currentChart.update('none');
}

function resetZoom() {
    if (!currentChart) return;
   
    isZoomModeActive = false;
    currentZoomMode = null;
    currentZoomLevel = 2;
    currentChart.resetZoom();
    currentChart.options.plugins.zoom.zoom.drag.enabled = false;
    currentChart.update('none');
   
    updateZoomButtonState('reset');
}

function updateZoomButtonState(mode) {
    const zoomInBtn = document.querySelector('.control-btn');
    const zoomOutBtn = document.querySelectorAll('.control-btn')[2];
   
    if (mode === 'in') {
        if (zoomInBtn && zoomInBtn.textContent.includes('🔍+')) {
            zoomInBtn.classList.add('active');
        }
        if (zoomOutBtn && zoomOutBtn.classList.contains('active')) {
            zoomOutBtn.classList.remove('active');
        }
    } else if (mode === 'out') {
        if (zoomOutBtn && zoomOutBtn.textContent.includes('🔍-')) {
            zoomOutBtn.classList.add('active');
        }
        if (zoomInBtn && zoomInBtn.classList.contains('active')) {
            zoomInBtn.classList.remove('active');
        }
    } else if (mode === 'reset') {
        if (zoomInBtn && zoomInBtn.classList.contains('active')) {
            zoomInBtn.classList.remove('active');
        }
        if (zoomOutBtn && zoomOutBtn.classList.contains('active')) {
            zoomOutBtn.classList.remove('active');
        }
    }
}

// Enhanced Crosshair System with Fixed Display - FIXED
function initializeCrosshairDisplay() {
    const chartWrapper = document.querySelector('.chart-wrapper');
    if (!chartWrapper) return;
   
    // Remove old axis indicators
    if (axisIndicators.yIndicator) axisIndicators.yIndicator.remove();
    if (axisIndicators.xIndicator) axisIndicators.xIndicator.remove();
   
    // Create fixed crosshair display
    let crosshairDisplay = document.getElementById('crosshairDisplay');
    if (!crosshairDisplay) {
        crosshairDisplay = document.createElement('div');
        crosshairDisplay.id = 'crosshairDisplay';
        crosshairDisplay.className = 'crosshair-display';
        crosshairDisplay.style.display = 'none';
        chartWrapper.appendChild(crosshairDisplay);
    }
}

function updateCrosshairDisplay(price, time) {
    const crosshairDisplay = document.getElementById('crosshairDisplay');
    if (!crosshairDisplay) return;
   
    if (price !== null && time) {
        crosshairDisplay.innerHTML = `
            <div class="crosshair-price">${price.toFixed(5)}</div>
            <div class="crosshair-time">${time}</div>
        `;
        crosshairDisplay.style.display = 'block';
       
        // Position in top-left corner
        const chartArea = currentChart?.chartArea;
        if (chartArea) {
            crosshairDisplay.style.top = `${chartArea.top + 10}px`;
            crosshairDisplay.style.left = `${chartArea.left + 10}px`;
        }
    } else {
        crosshairDisplay.style.display = 'none';
    }
}

function hideCrosshairDisplay() {
    const crosshairDisplay = document.getElementById('crosshairDisplay');
    if (crosshairDisplay) {
        crosshairDisplay.style.display = 'none';
    }
}

function addCrosshairListeners() {
    const canvas = document.getElementById('mainChart');
    if (!canvas) return;
   
    canvas.addEventListener('mousemove', function(event) {
        if (tooltipLocked || !crosshairEnabled || !currentChart) return;
       
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
       
        const chartArea = currentChart.chartArea;
        const yScale = currentChart.scales.y;
        const xScale = currentChart.scales.x;
       
        if (yScale && xScale && chartArea) {
            const price = yScale.getValueForPixel(y);
            const timeValue = xScale.getValueForPixel(x);
            const timeText = timeValue ? new Date(timeValue).toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            }) : '';
           
            updateCrosshairDisplay(price, timeText);
            updateCurrentPrice(price);
        }
       
        if (currentChart) currentChart.draw();
    });
   
    canvas.addEventListener('mouseleave', function() {
        hideCrosshairDisplay();
        if (currentChart) currentChart.draw();
    });
   
    if (currentChart) {
        const originalDraw = currentChart.draw;
        currentChart.draw = function() {
            originalDraw.call(this);
            if (crosshairEnabled) drawCrosshair();
        };
    }
}

function drawCrosshair() {
    if (!crosshairEnabled || !crosshairVisible || !currentChart) return;
    const ctx = currentChart.ctx;
    const chartArea = currentChart.chartArea;
   
    const boundedX = Math.max(chartArea.left, Math.min(chartArea.right, crosshairX));
    const boundedY = Math.max(chartArea.top, Math.min(chartArea.bottom, crosshairY));
   
    if (boundedX < chartArea.left || boundedX > chartArea.right || boundedY < chartArea.top || boundedY > chartArea.bottom) return;
   
    ctx.save();
    ctx.strokeStyle = '#E2E8F0';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
   
    ctx.beginPath();
    ctx.moveTo(boundedX, chartArea.top);
    ctx.lineTo(boundedX, chartArea.bottom);
    ctx.stroke();
   
    ctx.beginPath();
    ctx.moveTo(chartArea.left, boundedY);
    ctx.lineTo(chartArea.right, boundedY);
    ctx.stroke();
   
    ctx.restore();
}

// Chart controls and utilities
function setChartType(type) {
    currentChartType = type;
   
    const chartTypeSelect = document.getElementById('chartTypeSelect');
    if (chartTypeSelect) {
        chartTypeSelect.value = type;
    }
   
    if (currentTimeframe) {
        loadChart(currentTimeframe);
    }
}

function updateChartTimeframe() {
    const timeframe = document.getElementById('timeframeSelect').value;
    loadChart(timeframe);
}

function toggleCrosshair() {
    crosshairEnabled = !crosshairEnabled;
    const crosshairBtn = document.querySelector('.control-btn');
   
    if (crosshairBtn && crosshairBtn.textContent.includes('Cross')) {
        crosshairBtn.classList.toggle('active', crosshairEnabled);
    }
   
    if (!crosshairEnabled) {
        hideCrosshairDisplay();
    }
   
    if (currentChart) currentChart.draw();
}

function downloadChart() {
    if (!currentChart) return;
   
    const canvas = document.getElementById('mainChart');
    const link = document.createElement('a');
    link.download = `chart-${currentPair}-${currentTimeframe}-${new Date().toISOString().split('T')[0]}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}

// Chart time utilities
function getProfessionalTimeUnit(timeframe) {
    const units = {
        'M1': 'minute', 'M5': 'minute', 'M15': 'minute',
        'H1': 'hour', 'H4': 'hour', 'D1': 'day'
    };
    return units[timeframe] || 'hour';
}

function getProfessionalTimeFormats(timeframe) {
    return {
        minute: 'HH:mm',
        hour: 'MMM dd HH:mm',
        day: 'MMM dd, yyyy'
    };
}

// Current price display - FIXED
function updateCurrentPrice(price) {
    const currentPriceElement = document.getElementById('currentPrice');
    if (currentPriceElement && price) {
        const currentPriceValue = typeof price === 'number' ? price.toFixed(5) : price;
        currentPriceElement.textContent = currentPriceValue;
       
        const lastPrice = parseFloat(currentPriceElement.dataset.lastPrice) || price;
        let direction = 'neutral';
       
        if (price > lastPrice) {
            currentPriceElement.style.color = 'var(--green)';
            currentPriceElement.style.borderColor = 'var(--green-border)';
            direction = 'up';
        } else if (price < lastPrice) {
            currentPriceElement.style.color = 'var(--red)';
            currentPriceElement.style.borderColor = 'var(--red-border)';
            direction = 'down';
        } else {
            currentPriceElement.style.color = 'var(--gray)';
            currentPriceElement.style.borderColor = 'var(--gray-border)';
        }
       
        currentPriceElement.dataset.lastPrice = price;
        updateCurrentPriceLevel(price, direction);
    }
}
// ==================== INDICATORS MANAGEMENT ====================

function initializeIndicatorsPanel() {
    renderIndicatorsList();
}

function toggleIndicatorsPanel() {
    const panel = document.getElementById('indicatorsPanel');
    const toggleBtn = document.querySelector('.panel-toggle');
    
    if (panel.classList.contains('collapsed')) {
        panel.classList.remove('collapsed');
        if (toggleBtn) toggleBtn.innerHTML = '◀';
    } else {
        panel.classList.add('collapsed');
        if (toggleBtn) toggleBtn.innerHTML = '▶';
    }
}

function addIndicatorFromDropdown(indicatorType) {
    if (!indicatorType) return;
    
    const dropdown = document.getElementById('indicatorsDropdown');
    if (dropdown) dropdown.value = '';
    
    const instanceNumber = getNextAvailableInstanceNumber(indicatorType);
    const indicatorId = `${indicatorType}_${instanceNumber}`;
    
    const baseConfig = getIndicatorBaseConfig(indicatorType);
    if (!baseConfig) return;
    
    activeIndicators.set(indicatorId, { 
        ...baseConfig, 
        id: indicatorId,
        instanceNumber: instanceNumber,
        visible: true,
        settingsVisible: true
    });
    
    indicatorInstances[indicatorType].push(instanceNumber);
    renderIndicatorsList();
    
    if (currentTimeframe) {
        loadChart(currentTimeframe);
    }
    
    console.log(`✅ Added indicator: ${indicatorType} #${instanceNumber}`);
}

function getNextAvailableInstanceNumber(indicatorType) {
    const instances = indicatorInstances[indicatorType];
    if (instances.length === 0) return 1;
    
    for (let i = 1; i <= instances.length + 1; i++) {
        if (!instances.includes(i)) return i;
    }
    
    return Math.max(...instances) + 1;
}

function getIndicatorBaseConfig(type) {
    const baseConfigs = {
        'sma': { name: 'SMA', period: 20, color: '#00D394', minPeriod: 1, maxPeriod: 200 },
        'ema': { name: 'EMA', period: 12, color: '#3A86FF', minPeriod: 1, maxPeriod: 200 },
        'rsi': { name: 'RSI', period: 14, color: '#F59E0B', minPeriod: 1, maxPeriod: 50, yAxis: 'y2' },
        'macd': { name: 'MACD', fastPeriod: 12, slowPeriod: 26, signalPeriod: 9, color: '#10B981', minPeriod: 1, maxPeriod: 50 },
        'bollinger': { name: 'Bollinger', period: 20, stdDev: 2, color: '#EF4444', minPeriod: 1, maxPeriod: 50 },
        'stochastic': { name: 'Stochastic', kPeriod: 14, kSmooth: 3, dSmooth: 3, color: '#8B5CF6', minPeriod: 1, maxPeriod: 50, yAxis: 'y2' },
        'supportresistance': { name: 'Support/Resistance', supportColor: '#00D394', resistanceColor: '#FF4D4D' }
    };
    return baseConfigs[type];
}

function removeIndicator(indicatorId) {
    if (activeIndicators.has(indicatorId)) {
        const indicator = activeIndicators.get(indicatorId);
        const indicatorType = indicatorId.split('_')[0];
        const instanceNumber = indicator.instanceNumber;
        
        indicatorInstances[indicatorType] = indicatorInstances[indicatorType].filter(
            num => num !== instanceNumber
        );
        
        activeIndicators.delete(indicatorId);
        renderIndicatorsList();
        
        if (currentTimeframe) {
            loadChart(currentTimeframe);
        }
        console.log(`🗑️ Removed indicator: ${indicatorId}`);
    }
}

function updateIndicatorSetting(indicatorId, setting, value) {
    const indicator = activeIndicators.get(indicatorId);
    if (indicator) {
        if (setting.includes('Period') || setting === 'period' || setting === 'stdDev' || setting === 'kSmooth' || setting === 'dSmooth') {
            value = parseInt(value);
            const minVal = indicator.minPeriod || 1;
            const maxVal = indicator.maxPeriod || 200;
            if (value < minVal) value = minVal;
            if (value > maxVal) value = maxVal;
        }
        
        indicator[setting] = value;
        activeIndicators.set(indicatorId, indicator);
        
        if (currentTimeframe) {
            loadChart(currentTimeframe);
        }
    }
}

function toggleIndicatorSettings(indicatorId) {
    const indicator = activeIndicators.get(indicatorId);
    if (indicator) {
        indicator.settingsVisible = !indicator.settingsVisible;
        activeIndicators.set(indicatorId, indicator);
        renderIndicatorsList();
        console.log(`⚙️ Toggled settings for: ${indicatorId}`);
    }
}

function renderIndicatorsList() {
    const indicatorsList = document.getElementById('indicatorsList');
    if (!indicatorsList) return;

    if (activeIndicators.size === 0) {
        indicatorsList.innerHTML = '<div class="no-indicators">No indicators added</div>';
        return;
    }

    indicatorsList.innerHTML = Array.from(activeIndicators.entries()).map(([id, config]) => {
        const value = getIndicatorDisplayValue(id, config);
        const settingsHtml = generateIndicatorSettings(id, config);
        
        return `
            <div class="indicator-item ${config.visible ? 'active' : ''}">
                <div class="indicator-header" onclick="toggleIndicatorSettings('${id}')">
                    <div class="indicator-title">
                        <span class="indicator-status">●</span>
                        ${config.name} #${config.instanceNumber}
                    </div>
                    <div class="indicator-value">${value}</div>
                </div>
                ${config.settingsVisible ? `
                    <div class="indicator-settings">
                        ${settingsHtml}
                        <div class="indicator-actions">
                            <button class="indicator-btn remove" onclick="removeIndicator('${id}')">Remove Line</button>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

function generateIndicatorSettings(indicatorId, config) {
    const baseType = indicatorId.split('_')[0];
    
    switch(baseType) {
        case 'sma': case 'ema': case 'rsi':
            return `
                <div class="setting-group">
                    <label>Period:</label>
                    <input type="number" value="${config.period}" min="${config.minPeriod}" max="${config.maxPeriod}" onchange="updateIndicatorSetting('${indicatorId}', 'period', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>Color:</label>
                    <input type="color" value="${config.color}" onchange="updateIndicatorSetting('${indicatorId}', 'color', this.value)">
                </div>
            `;
        case 'macd':
            return `
                <div class="setting-group">
                    <label>Fast Period:</label>
                    <input type="number" value="${config.fastPeriod}" min="1" max="50" onchange="updateIndicatorSetting('${indicatorId}', 'fastPeriod', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>Slow Period:</label>
                    <input type="number" value="${config.slowPeriod}" min="1" max="50" onchange="updateIndicatorSetting('${indicatorId}', 'slowPeriod', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>Signal Period:</label>
                    <input type="number" value="${config.signalPeriod}" min="1" max="50" onchange="updateIndicatorSetting('${indicatorId}', 'signalPeriod', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>Color:</label>
                    <input type="color" value="${config.color}" onchange="updateIndicatorSetting('${indicatorId}', 'color', this.value)">
                </div>
            `;
        case 'bollinger':
            return `
                <div class="setting-group">
                    <label>Period:</label>
                    <input type="number" value="${config.period}" min="1" max="50" onchange="updateIndicatorSetting('${indicatorId}', 'period', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>Std Dev:</label>
                    <input type="number" value="${config.stdDev}" min="1" max="5" step="0.1" onchange="updateIndicatorSetting('${indicatorId}', 'stdDev', parseFloat(this.value))">
                </div>
                <div class="setting-group">
                    <label>Color:</label>
                    <input type="color" value="${config.color}" onchange="updateIndicatorSetting('${indicatorId}', 'color', this.value)">
                </div>
            `;
        case 'stochastic':
            return `
                <div class="setting-group">
                    <label>%K Period:</label>
                    <input type="number" value="${config.kPeriod}" min="1" max="50" onchange="updateIndicatorSetting('${indicatorId}', 'kPeriod', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>%K Smooth:</label>
                    <input type="number" value="${config.kSmooth}" min="1" max="10" onchange="updateIndicatorSetting('${indicatorId}', 'kSmooth', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>%D Smooth:</label>
                    <input type="number" value="${config.dSmooth}" min="1" max="10" onchange="updateIndicatorSetting('${indicatorId}', 'dSmooth', parseInt(this.value))">
                </div>
                <div class="setting-group">
                    <label>Color:</label>
                    <input type="color" value="${config.color}" onchange="updateIndicatorSetting('${indicatorId}', 'color', this.value)">
                </div>
            `;
        case 'supportresistance':
            return `
                <div class="setting-group">
                    <label>Support Color:</label>
                    <input type="color" value="${config.supportColor}" onchange="updateIndicatorSetting('${indicatorId}', 'supportColor', this.value)">
                </div>
                <div class="setting-group">
                    <label>Resistance Color:</label>
                    <input type="color" value="${config.resistanceColor}" onchange="updateIndicatorSetting('${indicatorId}', 'resistanceColor', this.value)">
                </div>
            `;
        default:
            return `
                <div class="setting-group">
                    <label>Color:</label>
                    <input type="color" value="${config.color}" onchange="updateIndicatorSetting('${indicatorId}', 'color', this.value)">
                </div>
            `;
    }
}

function getIndicatorDisplayValue(indicatorId, config) {
    const baseType = indicatorId.split('_')[0];
    
    switch(baseType) {
        case 'bollinger':
            const bbMiddle = currentIndicatorValues.bb_middle;
            return bbMiddle ? `BB: ${bbMiddle.toFixed(5)}` : '--';
        case 'stochastic':
            const stochK = currentIndicatorValues.stoch_k;
            const stochD = currentIndicatorValues.stoch_d;
            if (stochK && stochD) return `K:${stochK.toFixed(1)} D:${stochD.toFixed(1)}`;
            return '--';
        case 'macd':
            const macd = currentIndicatorValues.macd;
            const macdSignal = currentIndicatorValues.macd_signal;
            if (macd && macdSignal) return `MACD:${macd.toFixed(4)} Signal:${macdSignal.toFixed(4)}`;
            return '--';
        case 'supportresistance':
            return 'Auto';
        default:
            const instanceNumber = config.instanceNumber;
            const valueKeys = [
                `${baseType}_${config.period}`, `${baseType}_${instanceNumber}`, baseType, `${baseType}_20`, `${baseType}_12`
            ];
            
            for (const key of valueKeys) {
                if (currentIndicatorValues && currentIndicatorValues[key] !== undefined) {
                    const value = currentIndicatorValues[key];
                    return typeof value === 'number' ? value.toFixed(4) : '--';
                }
            }
            return '--';
    }
}

// ==================== UTILITIES & HELPERS ====================

// Volume formatting
function formatVolume(volume) {
    if (!volume && volume !== 0) return '--';
    const numVolume = parseFloat(volume);
    if (numVolume >= 1000000) return `${(numVolume / 1000000).toFixed(1)}M`;
    if (numVolume >= 1000) return `${(numVolume / 1000).toFixed(1)}K`;
    return numVolume.toFixed(0);
}

// Color management
function initializeColorPickers() {
    updateColorPickers();
}

function updateColorPickers() {
    const colorPickers = document.getElementById('colorPickers');
    if (!colorPickers) return;

    let colorHTML = `
        <div class="color-picker">
            <label>Line Color:</label>
            <input type="color" id="lineColor" value="${chartColors.line}" onchange="updateChartColors()">
        </div>
    `;
    
    colorPickers.innerHTML = colorHTML;
    
    if (currentTimeframe && currentChart) {
        loadChart(currentTimeframe);
    }
}

function updateChartColors() {
    const lineColorInput = document.getElementById('lineColor');
    if (lineColorInput) chartColors.line = lineColorInput.value;
    
    chartColors.areaFill = 'rgba(58, 134, 255, 0.15)';
    
    if (currentTimeframe) {
        loadChart(currentTimeframe);
    }
}

// Current price display
function updateCurrentPrice(price) {
    const currentPriceElement = document.getElementById('currentPrice');
    if (currentPriceElement && price) {
        currentPriceElement.textContent = typeof price === 'number' ? price.toFixed(5) : price;
        
        const lastPrice = parseFloat(currentPriceElement.dataset.lastPrice) || price;
        if (price > lastPrice) {
            currentPriceElement.style.color = 'var(--green)';
            currentPriceElement.style.borderColor = 'var(--green-border)';
        } else if (price < lastPrice) {
            currentPriceElement.style.color = 'var(--red)';
            currentPriceElement.style.borderColor = 'var(--red-border)';
        }
        currentPriceElement.dataset.lastPrice = price;
    }
}

// Keyboard shortcuts
function handleKeyboardShortcuts(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case '=':
                e.preventDefault();
                zoomIn();
                break;
            case '-':
                e.preventDefault();
                zoomOut();
                break;
            case '0':
                e.preventDefault();
                resetZoom();
                break;
            case 's':
                e.preventDefault();
                downloadChart();
                break;
        }
    }
    
    // Additional shortcuts without modifier
    switch(e.key) {
        case 'c':
            if (!e.ctrlKey && !e.metaKey) {
                e.preventDefault();
                toggleCrosshair();
            }
            break;
        case 'i':
            if (!e.ctrlKey && !e.metaKey) {
                e.preventDefault();
                toggleIndicatorsPanel();
            }
            break;
    }
}

// ==================== EXPORT & STARTUP ====================

// Export functions for global access
window.MegaFlowzDashboard = {
    initializeDashboard,
    loadChart,
    updateDashboard,
    changePair,
    changePyramidStyle,
    setChartType,
    addIndicatorFromDropdown,
    removeIndicator,
    toggleCrosshair,
    downloadChart,
    getPollingStatus,
    onUserAction
};

// Global functions needed for HTML event handlers
window.toggleBlock = toggleBlock;
window.toggleIndicatorSettings = toggleIndicatorSettings;
window.updateIndicatorSetting = updateIndicatorSetting;
window.removeIndicator = removeIndicator;
window.setPyramidSize = setPyramidSize;
window.switchTab = switchTab;
window.updateChartTimeframe = updateChartTimeframe;
window.setChartType = setChartType;
window.toggleIndicatorsPanel = toggleIndicatorsPanel;
window.toggleCrosshair = toggleCrosshair;
window.downloadChart = downloadChart;
window.zoomIn = zoomIn;
window.zoomOut = zoomOut;
window.resetZoom = resetZoom;
window.addIndicatorFromDropdown = addIndicatorFromDropdown;
console.log("🚀 MEGA FLOWZ Dashboard Script Loaded Successfully!");
