# Implementation Guide for Test Gap Finder

## 🚀 Getting Started

This guide provides step-by-step instructions for implementing the Test Gap Finder skill with practical code examples and integration patterns.

## 📋 Prerequisites

### Required Tools

```bash
# JavaScript/TypeScript
npm install @babel/parser @babel/traverse lcov-parse xml2js

# Python
pip install coverage.py lxml astunparse

# Java
# Use JavaParser or Eclipse JDT
```

### Coverage Report Formats

- **LCOV**: `.info` files (JavaScript, C++)
- **Cobertura**: `coverage.xml` (Multi-language)
- **JaCoCo**: `jacoco.xml` (Java)
- **Istanbul**: `coverage-final.json` (JavaScript)

## 🔧 Core Implementation

### 1. Coverage Report Parser

```javascript
// coverage-parser.js
const lcovParse = require('lcov-parse');
const { parseStringPromise } = require('xml2js');

async function parseCoverageReport(filePath) {
  if (filePath.endsWith('.info')) {
    // Parse LCOV format
    const data = await lcovParse(filePath);
    return convertLcovToStandard(data);
  } else if (filePath.endsWith('.xml')) {
    // Parse Cobertura or JaCoCo format
    const xml = await fs.promises.readFile(filePath, 'utf8');
    const result = await parseStringPromise(xml);
    return convertXmlToStandard(result);
  }
}

function convertLcovToStandard(lcovData) {
  const coverage = {};
  
  lcovData.forEach(entry => {
    coverage[entry.file] = {
      lines: Object.fromEntries(
        entry.lines.details.map(line => [line.line, line.hit > 0])
      ),
      functions: entry.functions.found,
      branches: entry.branches.found
    };
  });
  
  return coverage;
}
```

### 2. Source Code Parser (AST Analysis)

```javascript
// ast-analyzer.js
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;

function analyzeSourceCode(sourceCode) {
  const ast = parser.parse(sourceCode, {
    sourceType: 'module',
    plugins: ['jsx', 'typescript', 'classProperties']
  });
  
  const analysis = {
    functions: [],
    conditionals: [],
    errorHandlers: [],
    complexity: 0
  };
  
  traverse(ast, {
    FunctionDeclaration(path) {
      analysis.functions.push({
        name: path.node.id.name,
        start: path.node.loc.start.line,
        end: path.node.loc.end.line,
        params: path.node.params.length
      });
    },
    
    IfStatement(path) {
      analysis.conditionals.push({
        type: 'if',
        line: path.node.loc.start.line,
        test: path.node.test,
        hasElse: !!path.node.alternate
      });
    },
    
    TryStatement(path) {
      if (path.node.handler) {
        analysis.errorHandlers.push({
          type: 'try-catch',
          line: path.node.loc.start.line,
          handlerLine: path.node.handler.loc.start.line
        });
      }
    }
  });
  
  // Calculate cyclomatic complexity
  analysis.complexity = calculateComplexity(ast);
  
  return analysis;
}

function calculateComplexity(ast) {
  let complexity = 1; // Base complexity
  
  traverse(ast, {
    IfStatement() { complexity++ },
    ForStatement() { complexity++ },
    WhileStatement() { complexity++ },
    DoWhileStatement() { complexity++ },
    SwitchCase() { complexity++ },
    ConditionalExpression() { complexity++ },
    LogicalExpression() { complexity += 0.5 }
  });
  
  return complexity;
}
```

### 3. Gap Detection Engine

```javascript
// gap-detector.js
function detectTestGaps(coverageData, astAnalysis, sourceCode) {
  const gaps = [];
  
  // 1. Find untested functions
  astAnalysis.functions.forEach(func => {
    const fileCoverage = coverageData[func.file];
    if (!fileCoverage) return;
    
    let untestedLines = 0;
    for (let line = func.start; line <= func.end; line++) {
      if (fileCoverage.lines[line] === false) {
        untestedLines++;
      }
    }
    
    if (untestedLines > 0) {
      gaps.push(createFunctionGap(func, untestedLines, sourceCode));
    }
  });
  
  // 2. Find untested conditionals
  astAnalysis.conditionals.forEach(cond => {
    if (!coverageData[cond.file]?.lines[cond.line]) {
      gaps.push(createConditionalGap(cond, sourceCode));
    }
  });
  
  // 3. Find untested error handlers
  astAnalysis.errorHandlers.forEach(handler => {
    if (!coverageData[handler.file]?.lines[handler.handlerLine]) {
      gaps.push(createErrorHandlerGap(handler, sourceCode));
    }
  });
  
  // 4. Prioritize gaps by risk
  return gaps.sort((a, b) => b.riskScore - a.riskScore);
}

function createFunctionGap(func, untestedLines, sourceCode) {
  const lines = sourceCode.split('\n');
  const funcCode = lines.slice(func.start - 1, func.end).join('\n');
  
  return {
    type: 'function',
    name: func.name,
    file: func.file,
    startLine: func.start,
    endLine: func.end,
    untestedLines,
    totalLines: func.end - func.start + 1,
    coverage: 100 - (untestedLines / (func.end - func.start + 1)) * 100,
    risk: getRiskLevel(func.name, untestedLines),
    riskScore: calculateRiskScore(func.name, untestedLines),
    suggestions: generateFunctionSuggestions(func, funcCode)
  };
}

function getRiskLevel(functionName, untestedLines) {
  const highRiskKeywords = ['payment', 'auth', 'security', 'transaction', 'validate'];
  
  if (highRiskKeywords.some(keyword => functionName.toLowerCase().includes(keyword))) {
    return 'high';
  }
  
  if (untestedLines > 20) {
    return 'high';
  }
  
  if (untestedLines > 10) {
    return 'medium';
  }
  
  return 'low';
}
```

### 4. Test Suggestion Generator

```javascript
// suggestion-generator.js
function generateFunctionSuggestions(func, funcCode) {
  const suggestions = [];
  
  // Basic test suggestion
  suggestions.push({
    description: `Test ${func.name} with valid inputs`,
    example: `test('${func.name} with valid inputs', () => {
  const result = ${func.name}(${func.params.map((_, i) => `validArg${i}`).join(', ')});
  expect(result).toBeDefined();
});`
  });
  
  // Error case suggestion
  if (func.params.length > 0) {
    suggestions.push({
      description: `Test ${func.name} with invalid inputs`,
      example: `test('${func.name} with invalid inputs', () => {
  expect(() => ${func.name}(${func.params.map((_, i) => `invalidArg${i}`).join(', ')})).toThrow();
});`
    });
  }
  
  // Edge case suggestion
  suggestions.push({
    description: `Test ${func.name} with edge cases`,
    example: `test('${func.name} with edge cases', () => {
  // Test with null, undefined, empty values
  // Test with maximum/minimum values
  // Test with unusual but valid inputs
});`
  });
  
  // Function-specific suggestions
  if (func.name.toLowerCase().includes('validate')) {
    suggestions.push({
      description: `Test validation failures`,
      example: `test('validation failures', () => {
  const invalidInputs = [null, undefined, '', -1, 'invalid'];
  invalidInputs.forEach(input => {
    expect(() => ${func.name}(input)).toThrow();
  });
});`
    });
  }
  
  return suggestions;
}

function generateConditionalSuggestions(conditional) {
  return [{
    description: `Test both branches of conditional at line ${conditional.line}`,
    example: `test('conditional branches at line ${conditional.line}', () => {
  // Test when condition is true
  const trueCase = ${generateTrueCase(conditional.test)};
  expect(functionUnderTest(trueCase)).toBeDefined();
  
  // Test when condition is false  
  const falseCase = ${generateFalseCase(conditional.test)};
  expect(functionUnderTest(falseCase)).toBeDefined();
});`
  }];
}

function generateErrorHandlerSuggestions(handler) {
  return [{
    description: `Test error handling at line ${handler.line}`,
    example: `test('error handling at line ${handler.line}', async () => {
  // Mock error condition
  mockErrorCondition();
  
  // Verify error is handled properly
  await expect(functionUnderTest()).rejects.toThrow();
  
  // Verify error logging/recovery
  expect(errorLogger.called).toBe(true);
});`
  }];
}
```

### 5. Report Generator

```javascript
// report-generator.js
function generateMarkdownReport(gaps, coverageSummary) {
  const highRisk = gaps.filter(gap => gap.risk === 'high');
  const mediumRisk = gaps.filter(gap => gap.risk === 'medium');
  const lowRisk = gaps.filter(gap => gap.risk === 'low');
  
  return `# Test Gap Analysis Report
Generated: ${new Date().toISOString()}

## 📈 Coverage Summary
- **Overall Coverage**: ${coverageSummary.overall}%
- **Lines Covered**: ${coverageSummary.linesCovered}/${coverageSummary.totalLines}
- **Functions Covered**: ${coverageSummary.functionsCovered}%
- **Branches Covered**: ${coverageSummary.branchesCovered}%

## 🚨 Critical Gaps (High Risk) - ${highRisk.length} found
${highRisk.map(gap => generateGapSection(gap)).join('\n\n')}

## ⚠️ Important Gaps (Medium Risk) - ${mediumRisk.length} found
${mediumRisk.map(gap => generateGapSection(gap)).join('\n\n')}

## ℹ️ Minor Gaps (Low Risk) - ${lowRisk.length} found
${lowRisk.map(gap => generateGapSection(gap)).join('\n\n')}

## 📊 Statistics
- **Total Gaps Found**: ${gaps.length}
- **High Risk**: ${highRisk.length}
- **Medium Risk**: ${mediumRisk.length}
- **Low Risk**: ${lowRisk.length}
- **Average Risk Score**: ${(gaps.reduce((sum, gap) => sum + gap.riskScore, 0) / gaps.length).toFixed(1)}

## 🎯 Recommendations
1. Focus on high-risk gaps first
2. Write tests for error conditions and edge cases
3. Consider adding integration tests for critical paths
4. Review test strategy for areas with many gaps
`;
}

function generateGapSection(gap) {
  return `### ${gap.name} - ${gap.file}:${gap.startLine}-${gap.endLine}
- **Risk**: ${gap.risk.charAt(0).toUpperCase() + gap.risk.slice(1)}
- **Coverage**: ${gap.coverage}% (${gap.untestedLines} lines untested)
- **Complexity**: ${gap.complexity || 'N/A'}
- **Risk Score**: ${gap.riskScore}/100

**Suggested Tests:**
${gap.suggestions.map((suggestion, i) => `
${i + 1}. **${suggestion.description}**

   "` + suggestion.example + '`').join('')}`;
}
```

## 🔄 Complete Workflow

```javascript
// main.js
const fs = require('fs');

async function analyzeTestGaps(coveragePath, sourcePath) {
  // 1. Parse coverage report
  const coverageData = await parseCoverageReport(coveragePath);
  
  // 2. Analyze source code
  const sourceFiles = getSourceFiles(sourcePath);
  const astResults = {};
  
  for (const file of sourceFiles) {
    const sourceCode = fs.readFileSync(file, 'utf8');
    astResults[file] = analyzeSourceCode(sourceCode);
  }
  
  // 3. Detect gaps
  const gaps = [];
  for (const file of sourceFiles) {
    const sourceCode = fs.readFileSync(file, 'utf8');
    const fileGaps = detectTestGaps(coverageData, astResults[file], sourceCode);
    gaps.push(...fileGaps);
  }
  
  // 4. Generate report
  const coverageSummary = calculateCoverageSummary(coverageData);
  const report = generateMarkdownReport(gaps, coverageSummary);
  
  return { gaps, report };
}

function getSourceFiles(sourcePath) {
  // Recursively find all source files
  // Return array of file paths
}

function calculateCoverageSummary(coverageData) {
  let totalLines = 0;
  let coveredLines = 0;
  let totalFunctions = 0;
  let coveredFunctions = 0;
  
  Object.values(coverageData).forEach(file => {
    totalLines += Object.keys(file.lines).length;
    coveredLines += Object.values(file.lines).filter(covered => covered).length;
    totalFunctions += file.functions;
    // coveredFunctions would come from function coverage data
  });
  
  return {
    overall: totalLines > 0 ? (coveredLines / totalLines * 100).toFixed(1) : 0,
    linesCovered: coveredLines,
    totalLines,
    functionsCovered: totalFunctions > 0 ? ((coveredFunctions / totalFunctions) * 100).toFixed(1) : 0,
    branchesCovered: '72.5' // Would calculate from branch coverage
  };
}
```

## 🎛️ Configuration

```javascript
// config.js
module.exports = {
  // Risk assessment configuration
  risk: {
    highThreshold: 70,
    mediumThreshold: 40,
    highRiskKeywords: ['payment', 'auth', 'security', 'transaction', 'validate', 'delete'],
    criticalFunctions: ['handlePayment', 'validateToken', 'processTransaction']
  },
  
  // Coverage thresholds
  coverage: {
    excellent: 90,
    good: 75,
    fair: 50,
    poor: 30
  },
  
  // File patterns
  patterns: {
    source: ['**/*.js', '**/*.ts', '**/*.jsx', '**/*.tsx'],
    test: ['**/*.test.js', '**/*.spec.js', '**/__tests__/**/*.js'],
    coverage: ['coverage/lcov.info', 'coverage/cobertura.xml', 'target/jacoco.xml']
  },
  
  // Integration settings
  ci: {
    githubToken: process.env.GITHUB_TOKEN,
    gitlabToken: process.env.GITLAB_TOKEN,
    commentOnPR: true,
    failOnCriticalGaps: false
  }
};
```

## 🔌 Integration Patterns

### 1. CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/test-gap-analysis.yml
name: Test Gap Analysis
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests with coverage
      run: npm test -- --coverage
    
    - name: Install Test Gap Finder
      run: npm install -g test-gap-finder
    
    - name: Analyze test gaps
      run: test-gap-finder analyze --coverage coverage/lcov.info --src src/ > gaps.md
    
    - name: Comment on PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const gaps = fs.readFileSync('gaps.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## Test Gap Analysis\n\n${gaps}`
          });
```

### 2. CLI Tool

```javascript
#!/usr/bin/env node
// test-gap-finder-cli.js

const { program } = require('commander');
const { analyzeTestGaps } = require('./main');

program
  .name('test-gap-finder')
  .description('Find missing test cases in your codebase')
  .version('1.0.0')

program.command('analyze')
  .description('Analyze test gaps')
  .option('-c, --coverage <path>', 'Path to coverage report')
  .option('-s, --src <path>', 'Path to source code')
  .option('-o, --output <path>', 'Output file path')
  .option('-f, --format <format>', 'Output format (markdown|json|text)', 'markdown')
  .action(async (options) => {
    try {
      const { report } = await analyzeTestGaps(options.coverage, options.src);
      
      if (options.output) {
        fs.writeFileSync(options.output, report);
        console.log(`Report written to ${options.output}`);
      } else {
        console.log(report);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program.command('check')
  .description('Quick check for critical gaps')
  .option('-c, --coverage <path>', 'Path to coverage report')
  .option('-s, --src <path>', 'Path to source code')
  .action(async (options) => {
    try {
      const { gaps } = await analyzeTestGaps(options.coverage, options.src);
      const criticalGaps = gaps.filter(gap => gap.risk === 'high');
      
      if (criticalGaps.length > 0) {
        console.log(`⚠️  Found ${criticalGaps.length} critical test gaps:`);
        criticalGaps.forEach(gap => {
          console.log(`  - ${gap.name} (${gap.file}:${gap.startLine})`);
        });
        process.exit(1);
      } else {
        console.log('✅ No critical test gaps found');
        process.exit(0);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program.parse();
```

### 3. VSCode Extension

```javascript
// extension.js
const vscode = require('vscode');
const { analyzeTestGaps } = require('./main');

function activate(context) {
  let disposable = vscode.commands.registerCommand('testGapFinder.analyze', async function () {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
      vscode.window.showErrorMessage('No workspace opened');
      return;
    }
    
    const workspacePath = workspaceFolders[0].uri.fsPath;
    
    try {
      // Find coverage report
      const coverageFiles = await vscode.workspace.findFiles('**/coverage/**/*.{info,xml}');
      if (coverageFiles.length === 0) {
        vscode.window.showErrorMessage('No coverage report found. Run tests with coverage first.');
        return;
      }
      
      const coveragePath = coverageFiles[0].fsPath;
      
      // Analyze gaps
      const { report } = await analyzeTestGaps(coveragePath, path.join(workspacePath, 'src'));
      
      // Show results
      const doc = await vscode.workspace.openTextDocument({
        content: report,
        language: 'markdown'
      });
      
      await vscode.window.showTextDocument(doc);
      
    } catch (error) {
      vscode.window.showErrorMessage(`Test Gap Analysis failed: ${error.message}`);
    }
  });
  
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
```

## 🧪 Testing Strategy

### Unit Tests

```javascript
// test-gap-finder.test.js
const { analyzeSourceCode, detectTestGaps, generateMarkdownReport } = require('./main');

describe('Test Gap Finder', () => {
  describe('AST Analysis', () => {
    test('parses functions correctly', () => {
      const code = `
        function add(a, b) {
          return a + b;
        }
        
        const subtract = (a, b) => a - b;
      `;
      
      const result = analyzeSourceCode(code);
      expect(result.functions.length).toBe(2);
      expect(result.functions[0].name).toBe('add');
    });
  });

  describe('Gap Detection', () => {
    test('identifies untested functions', () => {
      const coverageData = {
        'test.js': {
          lines: { 1: true, 2: true, 3: false, 4: false, 5: true }
        }
      };
      
      const astAnalysis = {
        functions: [{
          name: 'untestedFunction',
          file: 'test.js',
          start: 3,
          end: 4
        }]
      };
      
      const gaps = detectTestGaps(coverageData, astAnalysis, '');
      expect(gaps.length).toBe(1);
      expect(gaps[0].name).toBe('untestedFunction');
    });
  });

  describe('Report Generation', () => {
    test('generates proper markdown report', () => {
      const gaps = [{
        name: 'testFunction',
        file: 'test.js',
        startLine: 1,
        endLine: 5,
        risk: 'high',
        suggestions: [{ description: 'Test basic case', example: 'test(...)' }]
      }];
      
      const report = generateMarkdownReport(gaps, { overall: 50 });
      expect(report).toContain('# Test Gap Analysis Report');
      expect(report).toContain('testFunction');
    });
  });
});
```

### Integration Tests

```javascript
// integration.test.js
const fs = require('fs');
const path = require('path');
const { analyzeTestGaps } = require('./main');

describe('Integration Tests', () => {
  test('full workflow with sample project', async () => {
    const testProject = path.join(__dirname, 'test-projects', 'sample-app');
    const coveragePath = path.join(testProject, 'coverage', 'lcov.info');
    const sourcePath = path.join(testProject, 'src');
    
    const result = await analyzeTestGaps(coveragePath, sourcePath);
    
    expect(result.gaps.length).toBeGreaterThan(0);
    expect(result.report).toContain('Test Gap Analysis Report');
    
    // Verify report file can be created
    const reportPath = path.join(testProject, 'gap-report.md');
    fs.writeFileSync(reportPath, result.report);
    expect(fs.existsSync(reportPath)).toBe(true);
    fs.unlinkSync(reportPath);
  });
});
```

## 📦 Deployment Options

### 1. NPM Package

```json
// package.json
{
  "name": "test-gap-finder",
  "version": "1.0.0",
  "description": "Find missing test cases in your codebase",
  "main": "dist/index.js",
  "bin": {
    "test-gap-finder": "./dist/cli.js"
  },
  "scripts": {
    "build": "babel src --out-dir dist",
    "test": "jest",
    "pack": "npm run build && npm pack"
  },
  "keywords": ["testing", "coverage", "test-gaps", "quality"],
  "dependencies": {
    "@babel/parser": "^7.20.0",
    "@babel/traverse": "^7.20.0",
    "lcov-parse": "^1.0.0",
    "xml2js": "^3.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "babel-cli": "^7.0.0",
    "babel-preset-env": "^7.0.0"
  }
}
```

### 2. Docker Container

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### 3. Browser Extension

```javascript
// background.js for Chrome Extension
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyzeGaps') {
    // Analyze test gaps for current GitHub repository
    analyzeRepository(request.url)
      .then(result => sendResponse({ success: true, result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Async response
  }
});

async function analyzeRepository(repoUrl) {
  // Extract owner/repo from URL
  // Fetch coverage data from GitHub Actions
  // Run gap analysis
  // Return results
}
```

## 🔧 Optimization Techniques

### Performance Optimization

1. **Incremental Analysis**: Only analyze changed files
2. **Caching**: Cache AST and coverage data
3. **Parallel Processing**: Use worker threads for large codebases
4. **Lazy Loading**: Load files on demand

```javascript
// Incremental analysis example
async function analyzeIncremental(currentCoverage, previousCoverage, changedFiles) {
  const gaps = [];
  
  for (const file of changedFiles) {
    if (isCoverageChanged(currentCoverage[file], previousCoverage[file])) {
      const sourceCode = fs.readFileSync(file, 'utf8');
      const astAnalysis = analyzeSourceCode(sourceCode);
      const fileGaps = detectTestGaps(currentCoverage, astAnalysis, sourceCode);
      gaps.push(...fileGaps);
    }
  }
  
  return gaps;
}
```

### Accuracy Improvement

1. **Machine Learning**: Train on historical gap data
2. **Pattern Recognition**: Identify common gap patterns
3. **Context Awareness**: Consider file importance and usage
4. **User Feedback**: Incorporate developer feedback

```javascript
// Machine learning example (pseudo-code)
function trainGapDetector(trainingData) {
  const model = new RandomForestClassifier();
  
  // Features: function name, complexity, file type, usage patterns
  // Label: actual gap importance (from historical data)
  
  model.train(trainingData);
  return model;
}

function predictGapImportance(gap, model) {
  const features = extractFeatures(gap);
  return model.predict(features);
}
```

## 📚 Resources

### Coverage Tools
- **JavaScript**: [Istanbul](https://istanbul.js.org/), [nyc](https://github.com/istanbuljs/nyc)
- **Python**: [coverage.py](https://coverage.readthedocs.io/), [pytest-cov](https://pytest-cov.readthedocs.io/)
- **Java**: [JaCoCo](https://www.jacoco.org/jacoco/), [Cobertura](http://cobertura.github.io/cobertura/)
- **Multi-language**: [SonarQube](https://www.sonarqube.org/)

### AST Parsing
- **JavaScript**: [@babel/parser](https://babeljs.io/docs/babel-parser), [acorn](https://github.com/acornjs/acorn)
- **Python**: [ast module](https://docs.python.org/3/library/ast.html), [astunparse](https://pypi.org/project/astunparse/)
- **Java**: [JavaParser](https://javaparser.org/), [Eclipse JDT](https://www.eclipse.org/jdt/)

### Testing Frameworks
- **JavaScript**: [Jest](https://jestjs.io/), [Mocha](https://mochajs.org/)
- **Python**: [pytest](https://docs.pytest.org/), [unittest](https://docs.python.org/3/library/unittest.html)
- **Java**: [JUnit](https://junit.org/), [TestNG](https://testng.org/)

### CI/CD Integration
- **GitHub Actions**: [Documentation](https://docs.github.com/en/actions)
- **GitLab CI**: [Documentation](https://docs.gitlab.com/ee/ci/)
- **Jenkins**: [Documentation](https://www.jenkins.io/doc/)

This implementation guide provides a comprehensive foundation for building the Test Gap Finder skill with practical examples, integration patterns, and optimization strategies.