export const SUBJECT_ORDER = [
  "공공조달의이해",
  "공공조달계획분석",
  "공공계약관리",
  "공공조달관리실무",
] as const;

export const SUBJECT_LABELS: Record<string, string> = {
  공공조달의이해: "공공조달의 이해",
  공공조달계획분석: "공공조달 계획분석",
  공공계약관리: "공공계약관리",
  공공조달관리실무: "공공조달 관리실무",
};

export const EXAM_LABELS: Record<string, string> = {
  공공조달의이해: "1차",
  공공조달계획분석: "1차",
  공공계약관리: "1차",
  공공조달관리실무: "2차",
};

export const SUBJECT_ICONS: Record<string, string> = {
  공공조달의이해: "📦",
  공공조달계획분석: "📊",
  공공계약관리: "📝",
  공공조달관리실무: "🏗️",
};

export const SUBJECT_COLORS: Record<string, {
  bg: string; text: string; border: string; header: string;
  accent: string; accentBorder: string; gradientFrom: string; gradientTo: string;
}> = {
  공공조달의이해:     { bg: "bg-blue-50/80",    text: "text-blue-700",    border: "border-blue-200",    header: "bg-blue-700",    accent: "bg-blue-100",    accentBorder: "border-l-blue-400",    gradientFrom: "from-blue-500",    gradientTo: "to-blue-600" },
  공공조달계획분석:   { bg: "bg-teal-50/80",    text: "text-teal-700",    border: "border-teal-200",    header: "bg-teal-700",    accent: "bg-teal-100",    accentBorder: "border-l-teal-400",    gradientFrom: "from-teal-500",    gradientTo: "to-teal-600" },
  공공계약관리:       { bg: "bg-amber-50/80",   text: "text-amber-700",   border: "border-amber-200",   header: "bg-amber-700",   accent: "bg-amber-100",   accentBorder: "border-l-amber-400",   gradientFrom: "from-amber-500",   gradientTo: "to-amber-600" },
  공공조달관리실무:   { bg: "bg-violet-50/80",  text: "text-violet-700",  border: "border-violet-200",  header: "bg-violet-700",  accent: "bg-violet-100",  accentBorder: "border-l-violet-400",  gradientFrom: "from-violet-500",  gradientTo: "to-violet-600" },
};

export function getSubjectColor(subject: string) {
  return SUBJECT_COLORS[subject] || {
    bg: "bg-gray-50", text: "text-gray-700", border: "border-gray-200", header: "bg-gray-700",
    accent: "bg-gray-100", accentBorder: "border-l-gray-400", gradientFrom: "from-gray-500", gradientTo: "to-gray-600",
  };
}
