import React from "react";

interface CodeBlockProps {
  code: string | object;
  language?: "json" | "jwt" | "logs" | "text";
  maxHeight?: string;
}

export default function CodeBlock({ code, language = "json", maxHeight = "max-h-60" }: CodeBlockProps) {
  const formatJson = (val: string | object): string => {
    if (typeof val === "object") {
      return JSON.stringify(val, null, 2);
    }
    try {
      return JSON.stringify(JSON.parse(val), null, 2);
    } catch {
      return String(val);
    }
  };

  const renderHighlightedJson = (jsonString: string) => {
    // Simple robust tokenizer for JSON syntax coloring
    const tokenRegex = /("(\\u[a-fA-F0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|[{}[\],:])/g;
    
    const lines = jsonString.split("\n");
    return lines.map((line, lineIdx) => {
      let match;
      const spans: React.ReactNode[] = [];
      let lastIndex = 0;

      // Reset regex for each line or run line-by-line
      const lineTokens: { text: string; type: string }[] = [];
      
      // Use match to split the line into colored parts
      const tokens = line.matchAll(tokenRegex);
      let currentPos = 0;

      for (const t of tokens) {
        const tokenText = t[0];
        const tokenPos = t.index!;

        // Add any plain whitespace or characters before this token
        if (tokenPos > currentPos) {
          lineTokens.push({
            text: line.substring(currentPos, tokenPos),
            type: "whitespace",
          });
        }

        // Determine token type
        let type = "punctuation";
        if (tokenText.startsWith('"')) {
          if (tokenText.endsWith(":")) {
            type = "key";
          } else {
            type = "string";
          }
        } else if (/^(true|false)$/.test(tokenText)) {
          type = "boolean";
        } else if (tokenText === "null") {
          type = "null";
        } else if (/^-?\d+/.test(tokenText)) {
          type = "number";
        }

        lineTokens.push({ text: tokenText, type });
        currentPos = tokenPos + tokenText.length;
      }

      // Add trailing characters
      if (currentPos < line.length) {
        lineTokens.push({
          text: line.substring(currentPos),
          type: "whitespace",
        });
      }

      return (
        <div key={lineIdx} className="min-h-[1.25rem] font-mono text-xs leading-5">
          {lineTokens.map((tok, tokIdx) => {
            let className = "text-slate-300";
            if (tok.type === "key") {
              className = "text-indigo-300 font-semibold";
            } else if (tok.type === "string") {
              className = "text-emerald-300";
            } else if (tok.type === "number") {
              className = "text-amber-300";
            } else if (tok.type === "boolean" || tok.type === "null") {
              className = "text-purple-400 font-medium";
            } else if (tok.type === "punctuation") {
              className = "text-slate-500";
            }
            return (
              <span key={tokIdx} className={className}>
                {tok.text}
              </span>
            );
          })}
        </div>
      );
    });
  };

  const renderHighlightedJwt = (jwtString: string) => {
    const trimmed = jwtString.trim();
    const parts = trimmed.split(".");
    
    if (parts.length === 3) {
      return (
        <div className="font-mono text-xs leading-5 break-all whitespace-pre-wrap">
          <span className="text-red-400 font-semibold" title="JWT Header">{parts[0]}</span>
          <span className="text-slate-500">.</span>
          <span className="text-indigo-300 font-semibold" title="JWT Claims Payload">{parts[1]}</span>
          <span className="text-slate-500">.</span>
          <span className="text-emerald-400" title="JWT Cryptographic Signature">{parts[2]}</span>
        </div>
      );
    }
    
    // Fallback if not exactly 3 parts (maybe decoded JSON JWT format)
    return renderHighlightedJson(formatJson(trimmed));
  };

  const renderHighlightedLogs = (logText: string) => {
    const lines = logText.split("\n");
    return lines.map((line, idx) => {
      let lineClass = "text-slate-300";
      
      // Determine line type for log highlighting
      if (/ERROR|FAIL|CRITICAL|REJECTED|SIGNATURE INVALID/i.test(line)) {
        lineClass = "text-red-300 font-medium bg-red-950/10 px-1 rounded";
      } else if (/WARN|ALERT|WARNING|DEGRADED/i.test(line)) {
        lineClass = "text-amber-300 font-medium bg-amber-950/10 px-1 rounded";
      } else if (/SUCCESS|OK|VALID|APPROVED|HEALTHY|MATCH FOUND/i.test(line)) {
        lineClass = "text-emerald-300 font-medium bg-emerald-950/10 px-1 rounded";
      } else if (/ACTION|RESOLVE|STEP|HOP/i.test(line)) {
        lineClass = "text-indigo-300";
      } else if (/FALLBACK/i.test(line)) {
        lineClass = "text-purple-300";
      }

      return (
        <div key={idx} className={`font-mono text-xs leading-5 min-h-[1.25rem] ${lineClass}`}>
          {line}
        </div>
      );
    });
  };

  const rawString = typeof code === "string" ? code : formatJson(code);

  return (
    <div 
      className={`w-full bg-slate-950/90 border border-slate-850/60 rounded-xl p-4 overflow-auto font-mono ${maxHeight}`}
      style={{ contentVisibility: "auto" }}
    >
      {language === "json" && renderHighlightedJson(formatJson(code))}
      {language === "jwt" && renderHighlightedJwt(rawString)}
      {language === "logs" && renderHighlightedLogs(rawString)}
      {language === "text" && (
        <pre className="text-slate-300 text-xs leading-5 whitespace-pre-wrap">{rawString}</pre>
      )}
    </div>
  );
}
