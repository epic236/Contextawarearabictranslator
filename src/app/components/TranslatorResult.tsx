import { useLocation, useNavigate } from "react-router";
import { useEffect } from "react";

export function TranslatorResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const {
    inputText,
    dialect,
    dialectCode,
    confidence,
    allProbabilities,
    normalizedText,
    appliedRules,
    translation,
    ambiguities
  } = location.state || {};

  useEffect(() => {
    if (!dialect || !translation) {
      navigate("/");
    }
  }, [dialect, translation, navigate]);

  if (!dialect || !translation) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 py-8">
      <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl text-center mb-8 text-gray-800">
          Translation Result
        </h1>

        <div className="space-y-6">
          {/* Dialect Detection */}
          <div className="bg-indigo-50 border-l-4 border-indigo-600 p-4 rounded">
            <p className="text-sm text-gray-600 mb-1">Detected Dialect:</p>
            <p className="text-2xl text-indigo-700">{dialect}</p>
            {dialectCode && (
              <p className="text-sm text-gray-500 mt-1">Code: {dialectCode}</p>
            )}
            {confidence && (
              <p className="text-sm text-gray-500 mt-1">
                Confidence: {(confidence * 100).toFixed(1)}%
              </p>
            )}
          </div>

          {/* All Dialect Probabilities */}
          {allProbabilities && Object.keys(allProbabilities).length > 0 && (
            <div className="bg-gray-50 p-4 rounded border border-gray-200">
              <p className="text-sm text-gray-600 mb-3">All Dialect Scores:</p>
              <div className="space-y-2">
                {Object.entries(allProbabilities)
                  .sort(([, a], [, b]) => (b as number) - (a as number))
                  .map(([dialectName, prob]) => (
                    <div key={dialectName} className="flex items-center gap-3">
                      <span className="text-sm text-gray-700 w-24">{dialectName}:</span>
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-indigo-600 h-2 rounded-full"
                          style={{ width: `${(prob as number) * 100}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-600 w-12 text-right">
                        {((prob as number) * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {/* Original Text */}
          <div>
            <p className="text-sm text-gray-600 mb-2">Original Text:</p>
            <div className="bg-gray-50 p-4 rounded border border-gray-200">
              <p className="text-gray-800 text-lg" dir="rtl">{inputText}</p>
            </div>
          </div>

          {/* Normalization Rules */}
          {appliedRules && appliedRules.length > 0 && (
            <div>
              <p className="text-sm text-gray-600 mb-2">Applied Normalization Rules:</p>
              <div className="bg-yellow-50 p-4 rounded border border-yellow-200">
                <ul className="space-y-1">
                  {appliedRules.map((rule, idx) => (
                    <li key={idx} className="text-sm text-gray-700">
                      • {rule}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Normalized Text */}
          {normalizedText && normalizedText !== inputText && (
            <div>
              <p className="text-sm text-gray-600 mb-2">Normalized (MSA) Text:</p>
              <div className="bg-blue-50 p-4 rounded border border-blue-200">
                <p className="text-gray-800" dir="rtl">{normalizedText}</p>
              </div>
            </div>
          )}

          {/* Translation */}
          <div>
            <p className="text-sm text-gray-600 mb-2">English Translation:</p>
            <div className="bg-green-50 p-4 rounded border border-green-200">
              <p className="text-gray-800 text-lg">{translation}</p>
            </div>
          </div>

          {/* Ambiguities */}
          {ambiguities && ambiguities.length > 0 && (
            <div>
              <p className="text-sm text-gray-600 mb-2">Potential Ambiguities:</p>
              <div className="bg-orange-50 p-4 rounded border border-orange-200">
                {ambiguities.map((amb, idx) => (
                  <div key={idx} className="mb-2 last:mb-0">
                    <p className="text-sm text-gray-700">
                      <span className="font-semibold" dir="rtl">{amb.word}</span> could mean:
                    </p>
                    <ul className="ml-4 mt-1">
                      {amb.possible_meanings.map((meaning, mIdx) => (
                        <li key={mIdx} className="text-sm text-gray-600">• {meaning}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={() => navigate("/")}
            className="w-full py-3 px-6 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Translate Another
          </button>
        </div>
      </div>
    </div>
  );
}
