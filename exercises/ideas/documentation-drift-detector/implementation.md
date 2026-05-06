# Implementation Guide for Documentation Drift Detector

## 🚀 Getting Started

This guide provides step-by-step instructions for implementing the Documentation Drift Detector skill with practical code examples and integration patterns.

## 📋 Prerequisites

### Required Tools

```bash
# Documentation Parsing
npm install markdown-it remark parse5

# Code Analysis
npm install @babel/parser @babel/traverse typescript

# Text Processing
npm install natural lodash

# File System
npm install glob fs-extra
```

### Supported Formats

**Documentation**: Markdown, RST, HTML, AsciiDoc
**Code**: JavaScript, TypeScript, Python, Java, Go

## 🔧 Core Implementation

### 1. Documentation Parser

```javascript
// documentation-parser.js
const fs = require('fs');
const path = require('path');
const markdownIt = require('markdown-it');
const { remark } = require('remark');
const strip = require('strip-markdown');

class DocumentationParser {
  constructor() {
    this.md = markdownIt();
  }

  async parseDocumentation(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const content = fs.readFileSync(filePath, 'utf8');
    
    let parsed;
    switch (ext) {
      case '.md':
        parsed = this.parseMarkdown(content);
        break;
      case '.rst':
        parsed = this.parseRST(content);
        break;
      case '.html':
        parsed = this.parseHTML(content);
        break;
      case '.adoc':
      case '.asciidoc':
        parsed = this.parseAsciiDoc(content);
        break;
      default:
        parsed = this.parseText(content);
    }
    
    return {
      path: filePath,
      type: ext.substring(1),
      content: content,
      parsed: parsed,
      metadata: this.extractMetadata(parsed)
    };
  }

  parseMarkdown(content) {
    const tokens = this.md.parse(content, {});
    const text = strip(content);
    
    return {
      tokens,
      text,
      codeBlocks: this.extractCodeBlocks(tokens),
      references: this.extractReferences(tokens, content)
    };
  }

  extractCodeBlocks(tokens) {
    const codeBlocks = [];
    let currentBlock = null;
    
    tokens.forEach((token, index) => {
      if (token.type === 'fence' && token.tag === 'code') {
        if (token.nesting === 1) {
          currentBlock = {
            start: index,
            lang: token.info,
            content: ''
          };
        } else if (currentBlock) {
          currentBlock.end = index;
          currentBlock.content = tokens.slice(currentBlock.start + 1, currentBlock.end)
            .map(t => t.content)
            .join('\n');
          codeBlocks.push(currentBlock);
          currentBlock = null;
        }
      }
    });
    
    return codeBlocks;
  }

  extractReferences(tokens, content) {
    const references = {
      functions: [],
      classes: [],
      variables: [],
      files: [],
      versions: []
    };
    
    // Extract function references (e.g., functionName())
    const functionRegex = /\b(\w+)\(/g;
    let match;
    while ((match = functionRegex.exec(content)) !== null) {
      references.functions.push(match[1]);
    }
    
    // Extract class references (e.g., ClassName)
    const classRegex = /\b[A-Z]\w*/g;
    while ((match = classRegex.exec(content)) !== null) {
      if (!references.functions.includes(match[0])) {
        references.classes.push(match[0]);
      }
    }
    
    // Extract version references
    const versionRegex = /v\d+\.\d+\.\d+|version \d+\.\d+\.\d+/gi;
    while ((match = versionRegex.exec(content)) !== null) {
      references.versions.push(match[0]);
    }
    
    return references;
  }

  extractMetadata(parsed) {
    return {
      wordCount: parsed.text.split(/\s+/).length,
      codeBlockCount: parsed.codeBlocks.length,
      referenceCount: Object.values(parsed.references).flat().length
    };
  }
}

module.exports = DocumentationParser;
```

### 2. Code Analyzer

```javascript
// code-analyzer.js
const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const ts = require('typescript');

class CodeAnalyzer {
  analyzeCode(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const content = fs.readFileSync(filePath, 'utf8');
    
    let ast, analysis;
    
    switch (ext) {
      case '.js':
      case '.jsx':
        ast = parser.parse(content, { sourceType: 'module', plugins: ['jsx'] });
        analysis = this.analyzeJavaScript(ast);
        break;
      case '.ts':
      case '.tsx':
        ast = ts.createSourceFile(filePath, content, ts.ScriptTarget.Latest, true);
        analysis = this.analyzeTypeScript(ast);
        break;
      case '.py':
        analysis = this.analyzePython(content);
        break;
      case '.java':
        analysis = this.analyzeJava(content);
        break;
      case '.go':
        analysis = this.analyzeGo(content);
        break;
      default:
        analysis = this.basicAnalysis(content);
    }
    
    return {
      path: filePath,
      language: ext.substring(1),
      content: content,
      analysis: analysis
    };
  }

  analyzeJavaScript(ast) {
    const analysis = {
      functions: [],
      classes: [],
      exports: [],
      imports: [],
      deprecated: []
    };
    
    traverse(ast, {
      FunctionDeclaration(path) {
        analysis.functions.push({
          name: path.node.id.name,
          start: path.node.loc.start.line,
          end: path.node.loc.end.line,
          params: path.node.params.map(p => p.name),
          deprecated: this.checkDeprecated(path.node.leadingComments)
        });
      },
      
      ClassDeclaration(path) {
        analysis.classes.push({
          name: path.node.id.name,
          start: path.node.loc.start.line,
          end: path.node.loc.end.line,
          methods: [],
          deprecated: this.checkDeprecated(path.node.leadingComments)
        });
      },
      
      ExportNamedDeclaration(path) {
        if (path.node.declaration) {
          analysis.exports.push(path.node.declaration.id.name);
        }
      },
      
      ImportDeclaration(path) {
        analysis.imports.push({
          source: path.node.source.value,
          specs: path.node.specifiers.map(s => s.local.name)
        });
      }
    });
    
    return analysis;
  }

  checkDeprecated(comments) {
    if (!comments) return false;
    return comments.some(comment => 
      comment.value.includes('@deprecated') ||
      comment.value.includes('DEPRECATED')
    );
  }

  analyzeTypeScript(ast) {
    const analysis = {
      functions: [],
      classes: [],
      interfaces: [],
      types: [],
      exports: [],
      deprecated: []
    };
    
    // TypeScript analysis would go here
    // Similar to JavaScript but with type information
    
    return analysis;
  }

  basicAnalysis(content) {
    return {
      functions: this.extractFunctionNames(content),
      classes: this.extractClassNames(content),
      lines: content.split('\n').length
    };
  }

  extractFunctionNames(content) {
    const functionRegex = /function\s+(\w+)|const\s+(\w+)\s*=\s*[^=]+=>|def\s+(\w+)/g;
    const matches = [];
    let match;
    
    while ((match = functionRegex.exec(content)) !== null) {
      matches.push(match[1] || match[2] || match[3]);
    }
    
    return [...new Set(matches)]; // Remove duplicates
  }

  extractClassNames(content) {
    const classRegex = /class\s+(\w+)|interface\s+(\w+)|public\s+class\s+(\w+)/g;
    const matches = [];
    let match;
    
    while ((match = classRegex.exec(content)) !== null) {
      matches.push(match[1] || match[2] || match[3]);
    }
    
    return [...new Set(matches)];
  }
}

module.exports = CodeAnalyzer;
```

### 3. Drift Detector

```javascript
// drift-detector.js
const { NaturalLanguageUnderstandingV1 } = require('ibm-watson/natural-language-understanding');

class DriftDetector {
  constructor() {
    // Initialize NLP if available
    this.nlp = this.setupNLP();
  }

  setupNLP() {
    // This would set up natural language processing
    // For production, consider using Watson, spaCy, or similar
    return null; // Simplified for example
  }

  detectDrift(documentation, codeAnalysis) {
    const driftIssues = [];
    
    // 1. Check for outdated function references
    documentation.references.functions.forEach(funcRef => {
      if (!this.isFunctionInCode(funcRef, codeAnalysis)) {
        driftIssues.push(this.createOutdatedFunctionIssue(funcRef, documentation, codeAnalysis));
      }
    });
    
    // 2. Check for missing documentation
    codeAnalysis.analysis.functions.forEach(func => {
      if (!this.isFunctionDocumented(func.name, documentation)) {
        driftIssues.push(this.createMissingDocumentationIssue(func, documentation));
      }
    });
    
    // 3. Check code examples
    documentation.parsed.codeBlocks.forEach(block => {
      const exampleIssues = this.validateCodeExample(block, codeAnalysis);
      driftIssues.push(...exampleIssues);
    });
    
    // 4. Check version references
    documentation.references.versions.forEach(versionRef => {
      if (this.isVersionOutdated(versionRef)) {
        driftIssues.push(this.createVersionIssue(versionRef, documentation));
      }
    });
    
    // 5. Prioritize issues
    return driftIssues.sort((a, b) => b.severityScore - a.severityScore);
  }

  isFunctionInCode(functionName, codeAnalysis) {
    // Check if function exists in any analyzed code file
    return codeAnalysis.some(file => 
      file.analysis.functions.some(f => f.name === functionName && !f.deprecated)
    );
  }

  isFunctionDocumented(functionName, documentation) {
    // Check if function is referenced in documentation
    return documentation.references.functions.includes(functionName);
  }

  validateCodeExample(codeBlock, codeAnalysis) {
    const issues = [];
    
    // Simple syntax check (in production, use proper parser)
    try {
      if (codeBlock.lang === 'javascript' || codeBlock.lang === 'js') {
        parser.parse(codeBlock.content, { sourceType: 'module' });
      }
    } catch (error) {
      issues.push(this.createBrokenExampleIssue(codeBlock, error.message));
    }
    
    // Check for deprecated function usage
    const functionCalls = this.extractFunctionCalls(codeBlock.content);
    functionCalls.forEach(call => {
      const isDeprecated = codeAnalysis.some(file => 
        file.analysis.functions.some(f => f.name === call && f.deprecated)
      );
      
      if (isDeprecated) {
        issues.push(this.createDeprecatedUsageIssue(call, codeBlock));
      }
    });
    
    return issues;
  }

  extractFunctionCalls(content) {
    const functionCallRegex = /\b(\w+)\(/g;
    const matches = [];
    let match;
    
    while ((match = functionCallRegex.exec(content)) !== null) {
      matches.push(match[1]);
    }
    
    return matches;
  }

  isVersionOutdated(versionRef) {
    // In production, compare with current version from package.json or similar
    const currentVersion = '2.4.1'; // Would be dynamic
    
    // Simple version comparison (would use semver in production)
    const refVersion = versionRef.replace(/[vVersion\s]/gi, '');
    return refVersion !== currentVersion;
  }

  createOutdatedFunctionIssue(functionName, documentation, codeAnalysis) {
    // Find potential replacements
    const suggestions = this.findSimilarFunctions(functionName, codeAnalysis);
    
    return {
      type: 'outdated_api',
      severity: 'high',
      severityScore: 85,
      file: documentation.path,
      location: this.findReferenceLocation(functionName, documentation),
      issue: `Reference to outdated function: ${functionName}`,
      details: {
        functionName,
        currentAlternatives: suggestions
      },
      suggestions: [
        `Update documentation to use current API: ${suggestions.join(' or ')}`,
        `Remove references to ${functionName} which is no longer available`
      ],
      exampleFix: suggestions.length > 0 
        ? `Use ${suggestions[0]} instead of ${functionName}`
        : `Remove references to ${functionName}`
    };
  }

  createMissingDocumentationIssue(functionDef, documentation) {
    return {
      type: 'missing_documentation',
      severity: 'medium',
      severityScore: 60,
      file: `Code: ${functionDef.name} in ${functionDef.file}`,
      location: `Function defined at line ${functionDef.start}`,
      issue: `Missing documentation for ${functionDef.name}`,
      details: {
        functionName: functionDef.name,
        params: functionDef.params,
        file: functionDef.file
      },
      suggestions: [
        `Add documentation for ${functionDef.name} in appropriate section`,
        `Include parameter descriptions and usage examples`,
        `Document return values and error cases`
      ],
      exampleFix: `
## ${functionDef.name}

${functionDef.description || 'Description needed'}

**Parameters**:
- ${functionDef.params.map(p => `\`${p}\`: Description`).join('\n- ')}

**Returns**: Description of return value

**Example**:
\`\`\`javascript
const result = ${functionDef.name}(${functionDef.params.join(', ')});
\`\`\``
    };
  }

  createBrokenExampleIssue(codeBlock, error) {
    return {
      type: 'broken_example',
      severity: 'high',
      severityScore: 90,
      file: documentation.path,
      location: `Code block at line ${codeBlock.start}`,
      issue: `Broken code example: ${error}`,
      details: {
        language: codeBlock.lang,
        error: error
      },
      suggestions: [
        `Fix syntax errors in the code example`,
        `Test the example in actual environment`,
        `Update to match current API`
      ],
      exampleFix: `// Corrected example would go here`
    };
  }

  createDeprecatedUsageIssue(functionName, codeBlock) {
    return {
      type: 'deprecated_usage',
      severity: 'medium',
      severityScore: 65,
      file: documentation.path,
      location: `Code example at line ${codeBlock.start}`,
      issue: `Example uses deprecated function: ${functionName}`,
      details: {
        functionName,
        codeBlock: codeBlock.start
      },
      suggestions: [
        `Update example to use current API`,
        `Add note about deprecation`,
        `Show both old and new approaches`
      ],
      exampleFix: `// TODO: Update to use current API instead of ${functionName}`
    };
  }

  createVersionIssue(versionRef, documentation) {
    return {
      type: 'version_mismatch',
      severity: 'low',
      severityScore: 30,
      file: documentation.path,
      location: this.findReferenceLocation(versionRef, documentation),
      issue: `Outdated version reference: ${versionRef}`,
      details: {
        referencedVersion: versionRef,
        currentVersion: '2.4.1' // Would be dynamic
      },
      suggestions: [
        `Update version references to current version`,
        `Use dynamic version references where possible`,
        `Add note about version compatibility`
      ],
      exampleFix: `Current version is 2.4.1`
    };
  }

  findSimilarFunctions(functionName, codeAnalysis) {
    // Simple similarity matching (would use more sophisticated approach in production)
    const allFunctions = codeAnalysis.flatMap(file => file.analysis.functions.map(f => f.name));
    
    return allFunctions.filter(f => 
      f.includes(functionName) || 
      functionName.includes(f) ||
      this.levenshteinDistance(f, functionName) < 3
    );
  }

  levenshteinDistance(a, b) {
    // Simple Levenshtein distance implementation
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    
    const matrix = [];
    
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i-1) === a.charAt(j-1)) {
          matrix[i][j] = matrix[i-1][j-1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i-1][j-1] + 1,
            matrix[i][j-1] + 1,
            matrix[i-1][j] + 1
          );
        }
      }
    }
    
    return matrix[b.length][a.length];
  }

  findReferenceLocation(reference, documentation) {
    // In production, this would find the actual line number
    // For now, return a placeholder
    return 'Line unknown';
  }
}

module.exports = DriftDetector;
```

### 4. Report Generator

```javascript
// report-generator.js
class ReportGenerator {
  generateReport(driftIssues, documentationFiles, codeFiles) {
    const highSeverity = driftIssues.filter(issue => issue.severity === 'high');
    const mediumSeverity = driftIssues.filter(issue => issue.severity === 'medium');
    const lowSeverity = driftIssues.filter(issue => issue.severity === 'low');
    
    return `# Documentation Drift Analysis Report
Generated: ${new Date().toISOString()}

## 📊 Summary
- **Documentation Files Analyzed**: ${documentationFiles.length}
- **Code Files Analyzed**: ${codeFiles.length}
- **Total Drift Issues**: ${driftIssues.length}
- **High Severity**: ${highSeverity.length}
- **Medium Severity**: ${mediumSeverity.length}
- **Low Severity**: ${lowSeverity.length}

## 🚨 High Severity Issues
${highSeverity.map(issue => this.formatIssue(issue)).join('\n\n')}

## ⚠️ Medium Severity Issues
${mediumSeverity.map(issue => this.formatIssue(issue)).join('\n\n')}

## ℹ️ Low Severity Issues
${lowSeverity.map(issue => this.formatIssue(issue)).join('\n\n')}

## 📈 Statistics
- **Drift Rate**: ${(driftIssues.length / documentationFiles.length * 100).toFixed(1)}%
- **Average Severity Score**: ${(driftIssues.reduce((sum, issue) => sum + issue.severityScore, 0) / driftIssues.length).toFixed(1)}

## 🎯 Recommendations
1. Address high severity issues first
2. Review medium severity issues for next sprint
3. Schedule documentation review session
4. Consider adding drift detection to CI/CD pipeline
`;
  }

  formatIssue(issue) {
    return `### ${issue.issue}
- **File**: ${issue.file}
- **Location**: ${issue.location}
- **Type**: ${issue.type}
- **Severity**: ${issue.severity} (Score: ${issue.severityScore})

**Details**:
${Object.entries(issue.details).map(([key, value]) => `- ${key}: ${value}`).join('\n')}

**Suggestions**:
${issue.suggestions.map(suggestion => `- ${suggestion}`).join('\n')}

**Example Fix**:
\`\`\`
${issue.exampleFix}
\`\`\``;
  }

  generateMarkdownReport(driftIssues, documentationFiles, codeFiles) {
    return this.generateReport(driftIssues, documentationFiles, codeFiles);
  }

  generateJSONReport(driftIssues) {
    return JSON.stringify(driftIssues, null, 2);
  }
}

module.exports = ReportGenerator;
```

### 5. Main Workflow

```javascript
// main.js
const fs = require('fs');
const path = require('path');
const glob = require('glob');
const DocumentationParser = require('./documentation-parser');
const CodeAnalyzer = require('./code-analyzer');
const DriftDetector = require('./drift-detector');
const ReportGenerator = require('./report-generator');

class DocumentationDriftDetector {
  constructor(config = {}) {
    this.config = {
      docPatterns: ['docs/**/*.md', 'README.md'],
      codePatterns: ['src/**/*.js', 'lib/**/*.ts'],
      ...config
    };
    
    this.parser = new DocumentationParser();
    this.analyzer = new CodeAnalyzer();
    this.detector = new DriftDetector();
    this.reporter = new ReportGenerator();
  }

  async analyzeProject() {
    // 1. Find documentation files
    const docFiles = this.findFiles(this.config.docPatterns);
    
    // 2. Find code files
    const codeFiles = this.findFiles(this.config.codePatterns);
    
    // 3. Parse documentation
    const documentation = [];
    for (const file of docFiles) {
      try {
        const parsed = await this.parser.parseDocumentation(file);
        documentation.push(parsed);
      } catch (error) {
        console.warn(`Failed to parse ${file}: ${error.message}`);
      }
    }
    
    // 4. Analyze code
    const codeAnalysis = [];
    for (const file of codeFiles) {
      try {
        const analyzed = this.analyzer.analyzeCode(file);
        codeAnalysis.push(analyzed);
      } catch (error) {
        console.warn(`Failed to analyze ${file}: ${error.message}`);
      }
    }
    
    // 5. Detect drift
    const driftIssues = [];
    documentation.forEach(doc => {
      const issues = this.detector.detectDrift(doc, codeAnalysis);
      driftIssues.push(...issues);
    });
    
    // 6. Generate report
    const report = this.reporter.generateReport(driftIssues, documentation, codeAnalysis);
    
    return {
      documentation,
      codeAnalysis,
      driftIssues,
      report
    };
  }

  findFiles(patterns) {
    const files = [];
    patterns.forEach(pattern => {
      const matches = glob.sync(pattern, { nodir: true });
      files.push(...matches);
    });
    return files;
  }

  async generateReport(format = 'markdown') {
    const result = await this.analyzeProject();
    
    switch (format) {
      case 'json':
        return this.reporter.generateJSONReport(result.driftIssues);
      case 'markdown':
      default:
        return result.report;
    }
  }
}

module.exports = DocumentationDriftDetector;
```

## 🔄 Complete Workflow Example

```javascript
// example-usage.js
const DocumentationDriftDetector = require('./main');

async function exampleUsage() {
  const detector = new DocumentationDriftDetector({
    docPatterns: ['docs/**/*.md', 'README.md'],
    codePatterns: ['src/**/*.js']
  });

  const result = await detector.analyzeProject();
  
  console.log('Analysis complete!');
  console.log(`Found ${result.driftIssues.length} drift issues`);
  
  // Save report
  fs.writeFileSync('drift-report.md', result.report);
  console.log('Report saved to drift-report.md');
  
  // Generate JSON report
  const jsonReport = await detector.generateReport('json');
  fs.writeFileSync('drift-report.json', jsonReport);
}

exampleUsage().catch(console.error);
```

## 🎛️ Configuration

```javascript
// config.js
module.exports = {
  // File patterns
  docPatterns: [
    'docs/**/*.md',
    'docs/**/*.rst',
    'README.md',
    'CONTRIBUTING.md',
    'CHANGELOG.md'
  ],
  
  codePatterns: [
    'src/**/*.js',
    'src/**/*.ts',
    'lib/**/*.js',
    '!**/__tests__/**/*.js'
  ],
  
  // Exclusions
  exclusions: [
    '**/node_modules/**',
    '**/build/**',
    '**/dist/**',
    '**/archive/**',
    '**/legacy/**'
  ],
  
  // Severity thresholds
  severity: {
    high: 70,
    medium: 40,
    low: 0
  },
  
  // Integration settings
  github: {
    repo: 'myorg/myrepo',
    token: process.env.GITHUB_TOKEN,
    createIssues: true,
    issueLabels: ['documentation', 'drift']
  },
  
  // Output settings
  output: {
    format: 'markdown',
    detail: 'detailed',
    includeSuggestions: true
  }
};
```

## 🔌 Integration Patterns

### 1. CLI Tool

```javascript
#!/usr/bin/env node
// drift-detector-cli.js

const { program } = require('commander');
const fs = require('fs');
const DocumentationDriftDetector = require('./main');

program
  .name('drift-detector')
  .description('Detect documentation drift')
  .version('1.0.0')

program.command('analyze')
  .description('Analyze documentation drift')
  .option('-d, --docs <patterns>', 'Documentation file patterns', 'docs/**/*.md')
  .option('-c, --code <patterns>', 'Code file patterns', 'src/**/*.js')
  .option('-o, --output <path>', 'Output file path')
  .option('-f, --format <format>', 'Output format (markdown|json)', 'markdown')
  .action(async (options) => {
    try {
      const detector = new DocumentationDriftDetector({
        docPatterns: options.docs.split(','),
        codePatterns: options.code.split(',')
      });
      
      const result = await detector.analyzeProject();
      
      if (options.output) {
        fs.writeFileSync(options.output, result.report);
        console.log(`Report written to ${options.output}`);
      } else {
        console.log(result.report);
      }
      
      if (result.driftIssues.length > 0) {
        console.log(`\n⚠️  Found ${result.driftIssues.length} drift issues`);
        process.exit(1);
      } else {
        console.log('\n✅ No documentation drift detected');
        process.exit(0);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program.command('check')
  .description('Quick drift check for CI/CD')
  .option('-d, --docs <patterns>', 'Documentation file patterns')
  .option('-c, --code <patterns>', 'Code file patterns')
  .action(async (options) => {
    try {
      const detector = new DocumentationDriftDetector({
        docPatterns: options.docs.split(','),
        codePatterns: options.code.split(',')
      });
      
      const result = await detector.analyzeProject();
      const critical = result.driftIssues.filter(i => i.severity === 'high');
      
      if (critical.length > 0) {
        console.log(`⚠️  Found ${critical.length} critical drift issues`);
        critical.forEach(issue => {
          console.log(`  - ${issue.issue} (${issue.file})`);
        });
        process.exit(1);
      } else {
        console.log('✅ No critical documentation drift');
        process.exit(0);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program.parse();
```

### 2. GitHub Action

```yaml
# .github/workflows/drift-detection.yml
name: Documentation Drift Detection
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0' # Weekly on Sunday

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
    
    - name: Install Documentation Drift Detector
      run: npm install -g documentation-drift-detector
    
    - name: Run drift detection
      run: drift-detector analyze --docs "docs/**/*.md,README.md" --code "src/**/*.js" --output drift-report.md
    
    - name: Upload drift report
      uses: actions/upload-artifact@v3
      with:
        name: drift-report
        path: drift-report.md
    
    - name: Comment on PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('drift-report.md', 'utf8');
          const driftCount = (report.match(/## 🚨 High Severity/g) || []).length;
          
          if (driftCount > 0) {
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Documentation Drift Detected\n\nFound ${driftCount} high severity drift issues. Please review the [drift report](https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}).`
            });
          }
```

### 3. CI/CD Integration

```javascript
// ci-integration.js
const DocumentationDriftDetector = require('./main');

async function checkDocumentationDrift() {
  const detector = new DocumentationDriftDetector();
  const result = await detector.analyzeProject();
  
  const criticalIssues = result.driftIssues.filter(issue => issue.severity === 'high');
  
  if (criticalIssues.length > 0) {
    console.error(`❌ Documentation drift detected: ${criticalIssues.length} critical issues`);
    criticalIssues.forEach(issue => {
      console.error(`  - ${issue.issue} (${issue.file})`);
    });
    process.exit(1);
  }
  
  console.log('✅ No critical documentation drift detected');
  process.exit(0);
}

checkDocumentationDrift().catch(error => {
  console.error('Drift detection failed:', error.message);
  process.exit(1);
});
```

## 🧪 Testing Strategy

### Unit Tests

```javascript
// drift-detector.test.js
const DocumentationParser = require('./documentation-parser');
const CodeAnalyzer = require('./code-analyzer');
const DriftDetector = require('./drift-detector');

describe('Documentation Drift Detector', () => {
  describe('Documentation Parser', () => {
    test('parses markdown correctly', async () => {
      const parser = new DocumentationParser();
      const result = await parser.parseDocumentation('test-docs/test.md');
      
      expect(result.parsed.codeBlocks.length).toBeGreaterThan(0);
      expect(result.parsed.references.functions.length).toBeGreaterThan(0);
    });
  });

  describe('Code Analyzer', () => {
    test('analyzes JavaScript code', () => {
      const analyzer = new CodeAnalyzer();
      const result = analyzer.analyzeCode('test-code/test.js');
      
      expect(result.analysis.functions.length).toBeGreaterThan(0);
      expect(result.analysis.classes.length).toBeGreaterThan(0);
    });
  });

  describe('Drift Detector', () => {
    test('detects outdated function references', async () => {
      const parser = new DocumentationParser();
      const analyzer = new CodeAnalyzer();
      const detector = new DriftDetector();
      
      const doc = await parser.parseDocumentation('test-docs/outdated.md');
      const code = analyzer.analyzeCode('test-code/current.js');
      
      const drift = detector.detectDrift(doc, [code]);
      expect(drift.length).toBeGreaterThan(0);
      expect(drift[0].type).toBe('outdated_api');
    });

    test('identifies missing documentation', async () => {
      const parser = new DocumentationParser();
      const analyzer = new CodeAnalyzer();
      const detector = new DriftDetector();
      
      const doc = await parser.parseDocumentation('test-docs/complete.md');
      const code = analyzer.analyzeCode('test-code/new-feature.js');
      
      const drift = detector.detectDrift(doc, [code]);
      expect(drift.some(i => i.type === 'missing_documentation')).toBe(true);
    });
  });
});
```

### Integration Tests

```javascript
// integration.test.js
const DocumentationDriftDetector = require('./main');
const fs = require('fs');

describe('Integration Tests', () => {
  test('full workflow with test project', async () => {
    const detector = new DocumentationDriftDetector({
      docPatterns: ['test-project/docs/**/*.md'],
      codePatterns: ['test-project/src/**/*.js']
    });
    
    const result = await detector.analyzeProject();
    
    expect(result.documentation.length).toBeGreaterThan(0);
    expect(result.codeAnalysis.length).toBeGreaterThan(0);
    expect(result.driftIssues.length).toBeGreaterThan(0);
    expect(result.report).toContain('Documentation Drift Analysis Report');
    
    // Verify report can be saved
    const reportPath = 'test-output/drift-report.md';
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
  "name": "documentation-drift-detector",
  "version": "1.0.0",
  "description": "Detect outdated documentation in your codebase",
  "main": "dist/index.js",
  "bin": {
    "drift-detector": "./dist/cli.js"
  },
  "scripts": {
    "build": "babel src --out-dir dist",
    "test": "jest",
    "pack": "npm run build && npm pack"
  },
  "keywords": ["documentation", "drift", "quality", "maintenance"],
  "dependencies": {
    "markdown-it": "^13.0.0",
    "@babel/parser": "^7.20.0",
    "@babel/traverse": "^7.20.0",
    "glob": "^8.0.0",
    "lodash": "^4.17.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "babel-cli": "^7.0.0",
    "nock": "^13.0.0"
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

### 3. Serverless Function

```javascript
// AWS Lambda example
exports.handler = async (event) => {
  try {
    const detector = new DocumentationDriftDetector(event.config);
    const result = await detector.analyzeProject();
    
    return {
      statusCode: 200,
      body: JSON.stringify(result),
      headers: { 'Content-Type': 'application/json' }
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
```

## 🔧 Optimization Techniques

### Performance Optimization

1. **Incremental Analysis**: Only analyze changed files
2. **Caching**: Cache parsed documentation and code analysis
3. **Parallel Processing**: Use worker threads for large projects
4. **File Filtering**: Skip irrelevant files early

```javascript
// Incremental analysis example
class IncrementalDriftDetector extends DocumentationDriftDetector {
  constructor(config) {
    super(config);
    this.cache = new Map();
  }

  async analyzeProject(changedFiles = []) {
    if (changedFiles.length === 0) {
      return super.analyzeProject();
    }
    
    // Only analyze changed files and their dependencies
    const filesToAnalyze = this.getAffectedFiles(changedFiles);
    
    // Use cached results for unchanged files
    const result = await this.analyzeSpecificFiles(filesToAnalyze);
    
    return result;
  }

  getAffectedFiles(changedFiles) {
    // Determine which documentation and code files are affected
    // by the changes
  }
}
```

### Accuracy Improvement

1. **Machine Learning**: Train on historical drift data
2. **Pattern Recognition**: Identify common drift patterns
3. **Context Awareness**: Consider project structure
4. **User Feedback**: Incorporate corrections over time

```javascript
// Machine learning enhancement
class SmartDriftDetector extends DriftDetector {
  constructor() {
    super();
    this.feedback = [];
  }

  recordFeedback(original, corrected) {
    this.feedback.push({ original, corrected });
    
    if (this.feedback.length >= 100) {
      this.retrainModel();
    }
  }

  retrainModel() {
    // Retrain with accumulated feedback
    // Improve future drift detection
  }
}
```

## 📚 Resources

### Documentation Parsing
- [Markdown-it](https://github.com/markdown-it/markdown-it)
- [Remark](https://github.com/remarkjs/remark)
- [Parse5](https://github.com/inikulin/parse5)
- [CommonMark](https://commonmark.org/)

### Code Analysis
- [Babel Parser](https://babeljs.io/docs/babel-parser)
- [TypeScript Compiler API](https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API)
- [Python AST](https://docs.python.org/3/library/ast.html)
- [JavaParser](https://javaparser.org/)

### Natural Language Processing
- [Natural Node.js](https://github.com/NaturalNode/natural)
- [Compromise](https://github.com/spencermountain/compromise)
- [spaCy](https://spacy.io/)
- [IBM Watson NLP](https://www.ibm.com/watson/services/natural-language-understanding/)

### Documentation Tools
- [Docusaurus](https://docusaurus.io/)
- [Sphinx](https://www.sphinx-doc.org/)
- [MkDocs](https://www.mkdocs.org/)
- [GitBook](https://www.gitbook.com/)

This implementation guide provides a comprehensive foundation for building the Documentation Drift Detector skill with practical examples, integration patterns, and optimization strategies.