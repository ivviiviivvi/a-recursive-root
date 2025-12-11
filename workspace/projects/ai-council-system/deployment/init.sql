-- AI Council System - PostgreSQL Initialization Schema
-- Creates database tables for debates, streaming sessions, metrics, and analytics

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Debates table
CREATE TABLE IF NOT EXISTS debates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    debate_id VARCHAR(255) UNIQUE NOT NULL,
    topic TEXT NOT NULL,
    scheduled_time TIMESTAMP NOT NULL,
    actual_start_time TIMESTAMP,
    actual_end_time TIMESTAMP,
    duration_seconds INTEGER,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    participant_count INTEGER DEFAULT 0,
    round_count INTEGER DEFAULT 0,
    total_responses INTEGER DEFAULT 0,
    avg_response_length INTEGER,
    avg_confidence DECIMAL(5, 4),
    viewer_count_peak INTEGER DEFAULT 0,
    engagement_score DECIMAL(5, 4),
    consensus_level DECIMAL(5, 4),
    controversy_score DECIMAL(5, 4),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Streaming sessions table
CREATE TABLE IF NOT EXISTS streaming_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    debate_id UUID REFERENCES debates(id) ON DELETE SET NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    platforms TEXT[] NOT NULL,
    total_viewers_peak INTEGER DEFAULT 0,
    avg_bitrate_kbps INTEGER,
    total_bytes_sent BIGINT DEFAULT 0,
    uptime_percent DECIMAL(5, 2),
    frame_drop_rate DECIMAL(5, 2),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platform-specific streaming metrics
CREATE TABLE IF NOT EXISTS platform_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES streaming_sessions(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    viewer_count INTEGER DEFAULT 0,
    bitrate_kbps INTEGER,
    fps DECIMAL(5, 2),
    drop_rate_percent DECIMAL(5, 2),
    status VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Health check results
CREATE TABLE IF NOT EXISTS health_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    check_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    response_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- System metrics
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_percent DECIMAL(5, 2),
    memory_percent DECIMAL(5, 2),
    disk_percent DECIMAL(5, 2),
    network_bytes_sent BIGINT,
    network_bytes_received BIGINT,
    active_debates INTEGER DEFAULT 0,
    active_streams INTEGER DEFAULT 0,
    total_viewers INTEGER DEFAULT 0,
    metadata JSONB
);

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    component VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    acknowledged_by VARCHAR(255),
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    metadata JSONB
);

-- Voice cache metadata (for tracking cached audio files)
CREATE TABLE IF NOT EXISTS voice_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    personality_name VARCHAR(100) NOT NULL,
    text_hash VARCHAR(64) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    duration_seconds DECIMAL(10, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    metadata JSONB
);

-- Background rendering metadata
CREATE TABLE IF NOT EXISTS background_renders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    debate_id UUID REFERENCES debates(id) ON DELETE CASCADE,
    style VARCHAR(50) NOT NULL,
    mood VARCHAR(50) NOT NULL,
    sentiment_score DECIMAL(5, 4),
    frame_number INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Performance insights (aggregated analytics)
CREATE TABLE IF NOT EXISTS performance_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    total_debates INTEGER DEFAULT 0,
    total_streams INTEGER DEFAULT 0,
    avg_engagement DECIMAL(5, 4),
    avg_viewers INTEGER,
    system_health VARCHAR(50),
    highlights TEXT[],
    recommendations TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_debates_scheduled_time ON debates(scheduled_time);
CREATE INDEX IF NOT EXISTS idx_debates_status ON debates(status);
CREATE INDEX IF NOT EXISTS idx_debates_created_at ON debates(created_at);
CREATE INDEX IF NOT EXISTS idx_streaming_sessions_start_time ON streaming_sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_streaming_sessions_status ON streaming_sessions(status);
CREATE INDEX IF NOT EXISTS idx_platform_metrics_session_id ON platform_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_platform_metrics_platform ON platform_metrics(platform);
CREATE INDEX IF NOT EXISTS idx_platform_metrics_timestamp ON platform_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_health_checks_check_name ON health_checks(check_name);
CREATE INDEX IF NOT EXISTS idx_health_checks_timestamp ON health_checks(timestamp);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_component ON alerts(component);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(resolved);
CREATE INDEX IF NOT EXISTS idx_voice_cache_cache_key ON voice_cache(cache_key);
CREATE INDEX IF NOT EXISTS idx_voice_cache_personality ON voice_cache(personality_name);
CREATE INDEX IF NOT EXISTS idx_voice_cache_last_accessed ON voice_cache(last_accessed_at);
CREATE INDEX IF NOT EXISTS idx_background_renders_debate_id ON background_renders(debate_id);
CREATE INDEX IF NOT EXISTS idx_performance_insights_period ON performance_insights(period_start, period_end);

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update trigger to relevant tables
CREATE TRIGGER update_debates_updated_at BEFORE UPDATE ON debates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_streaming_sessions_updated_at BEFORE UPDATE ON streaming_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Voice cache access update trigger
CREATE OR REPLACE FUNCTION update_voice_cache_access()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_accessed_at = CURRENT_TIMESTAMP;
    NEW.access_count = OLD.access_count + 1;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_voice_cache_on_access BEFORE UPDATE ON voice_cache
    FOR EACH ROW
    WHEN (NEW.last_accessed_at = OLD.last_accessed_at)
    EXECUTE FUNCTION update_voice_cache_access();

-- Insert default data
INSERT INTO performance_insights (period_start, period_end, total_debates, total_streams, system_health, created_at)
VALUES (CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP, 0, 0, 'healthy', CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

-- Create views for common queries
CREATE OR REPLACE VIEW debate_summary AS
SELECT
    DATE(scheduled_time) as date,
    COUNT(*) as total_debates,
    AVG(duration_seconds) as avg_duration_seconds,
    AVG(participant_count) as avg_participants,
    AVG(engagement_score) as avg_engagement,
    SUM(viewer_count_peak) as total_peak_viewers,
    AVG(consensus_level) as avg_consensus,
    AVG(controversy_score) as avg_controversy
FROM debates
WHERE status = 'completed'
GROUP BY DATE(scheduled_time)
ORDER BY date DESC;

CREATE OR REPLACE VIEW streaming_summary AS
SELECT
    DATE(start_time) as date,
    COUNT(*) as total_sessions,
    SUM(duration_seconds) / 3600.0 as total_hours,
    AVG(total_viewers_peak) as avg_peak_viewers,
    AVG(avg_bitrate_kbps) as avg_bitrate_kbps,
    AVG(uptime_percent) as avg_uptime_percent,
    ARRAY_AGG(DISTINCT UNNEST(platforms)) as platforms_used
FROM streaming_sessions
WHERE status = 'completed'
GROUP BY DATE(start_time)
ORDER BY date DESC;

CREATE OR REPLACE VIEW system_health_current AS
SELECT
    check_name,
    status,
    message,
    response_time_ms,
    timestamp
FROM health_checks
WHERE timestamp > CURRENT_TIMESTAMP - INTERVAL '5 minutes'
ORDER BY timestamp DESC;

CREATE OR REPLACE VIEW active_alerts AS
SELECT
    component,
    severity,
    message,
    timestamp,
    acknowledged
FROM alerts
WHERE resolved = FALSE
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'error' THEN 2
        WHEN 'warning' THEN 3
        ELSE 4
    END,
    timestamp DESC;

-- Grant permissions (adjust user as needed)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO postgres;
