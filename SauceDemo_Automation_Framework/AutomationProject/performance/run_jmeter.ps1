param([string]$JMeter = "jmeter")
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $PSScriptRoot "jmeter_support"
$classes = Join-Path $sourceRoot "classes"
$source = Join-Path $sourceRoot "java/util/prefs/MemoryPreferencesFactory.java"
$out = Join-Path $PSScriptRoot "results"
$html = Join-Path $PSScriptRoot "html_report"
New-Item -ItemType Directory -Force -Path $classes,$out | Out-Null
javac --patch-module "java.prefs=$sourceRoot" -d $classes $source
if ($LASTEXITCODE -ne 0) { throw "Could not compile in-memory Preferences helper." }
if (Test-Path $html) { Remove-Item -LiteralPath $html -Recurse -Force }
New-Item -ItemType Directory -Force -Path $html | Out-Null
foreach ($name in @("results.jtl","aggregate.csv","jmeter.log")) {
    $file=Join-Path $out $name
    if (Test-Path $file) { Remove-Item -LiteralPath $file -Force }
}
$env:JVM_ARGS = "--patch-module=java.prefs=$classes -Djava.util.prefs.PreferencesFactory=java.util.prefs.MemoryPreferencesFactory"
Push-Location $root
try {
    & $JMeter -n -t "performance/jmx/saucedemo_weekend_lab.jmx" -l "performance/results/results.jtl" -j "performance/results/jmeter.log" -e -o "performance/html_report"
    if ($LASTEXITCODE -ne 0) { throw "JMeter failed with exit code $LASTEXITCODE" }
    & python "performance/summarize_jmeter.py"
    if ($LASTEXITCODE -ne 0) { throw "JMeter result summarization failed." }
} finally {
    Remove-Item Env:JVM_ARGS -ErrorAction SilentlyContinue
    Pop-Location
}
