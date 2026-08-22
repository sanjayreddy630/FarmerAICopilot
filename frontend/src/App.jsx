import { motion } from "framer-motion";

import {
  ArrowUpRight,
  ArrowLeft,
  Leaf,
  Paperclip,
  Camera,
  Mic,
  MicOff,
  Sparkles,
  ShieldCheck,
  Search,
  AlertTriangle,
  CheckCircle2,
  BookOpen,
} from "lucide-react";

import { useEffect, useRef, useState } from "react";

import "./App.css";

const UI_TEXT = {
  English: {
    copilot: "Copilot",
    technology: "Technology",
    rag: "RAG Intelligence",
    sources: "Sources",
    explore: "Explore",
    badge: "SOURCE-GROUNDED AGRICULTURAL INTELLIGENCE",
    heroTitle1: "Smarter farming.",
    heroTitle2: "Better decisions.",
    heroDescription: "Ask your farming questions naturally and receive AI-powered recommendations grounded in trusted agricultural knowledge.",
    upload: "Upload file",
    placeholder: "Ask Farmer AI anything...",
    stopVoice: "Stop voice input",
    speak: "Speak your question",
    camera: "Take a crop or pest photo",
    listening: "Listening...",
    uploading: "Uploading file...",
    hint: "Press Enter to ask • Powered by Hybrid RAG + AI",
    cropAware: "Crop aware",
    aiPowered: "AI powered",
    grounded: "Source grounded",
    intelligenceLayer: "THE INTELLIGENCE LAYER",
    notJustAI: "Not just AI.",
    agriculturalAI: "Agricultural AI.",
    aiReasoning: "AI Reasoning",
    aiReasoningText: "Understands natural farming language, symptoms, crops, seasons and context.",
    hybridRAG: "Hybrid RAG",
    hybridRAGText: "Retrieves and reranks the most relevant agricultural knowledge before generating an answer.",
    groundedAnswers: "Grounded Answers",
    groundedAnswersText: "Recommendations are generated from retrieved knowledge rather than unsupported guesses.",
    traceability: "Source Traceability",
    traceabilityText: "Every recommendation can be traced back to its supporting source and page.",
    back: "Back to Farmer AI",
    recommendation: "FARMER AI RECOMMENDATION",
    answered1: "Your farming question,",
    answered2: "answered.",
    problem: "Problem / Short Answer",
    check: "What to Check",
    action: "What to Do",
    precautions: "Precautions",
    source: "Sources",
    page: "Page",
    agriculturalSource: "Agricultural Knowledge Source",
    noInfo: "No specific information was provided.",
    cameraTitle: "Crop / Pest Camera",
    cameraSubtitle: "Take a clear photo of the affected plant",
    cancel: "Cancel",
    analyze: "Capture & Analyze",
    analyzing: "Analyzing...",
    imageAnalysis: "AI IMAGE ANALYSIS",
    pestDetected: "Pest detected",
    confidence: "Confidence",
    confidenceLevel: "Confidence level",
    topPredictions: "Top predictions",
    whatDo: "What should you do?",
    warning: "AI image analysis is a screening aid. Verify uncertain results with a local agricultural expert before applying pesticides.",
    done: "Done",
    footer: "• Hybrid RAG • Source-Grounded AI",
    voiceUnsupported: "Voice input is not supported in this browser. Please use Google Chrome or Microsoft Edge.",
    micBlocked: "Microphone permission is blocked. Click the microphone icon in Chrome's address bar and allow microphone access for localhost:5173.",
    micCapture: "Chrome could not access your microphone. Check your microphone connection and Windows microphone permissions.",
    speechNetwork: "Speech recognition could not connect to the speech service. Check your internet connection and try again.",
    voiceStart: "Could not start voice input. Please click the microphone again.",
    voiceInit: "Unable to initialize voice input. Please try again.",
    voiceError: "Voice input error. Please try again.",
    cameraUnsupported: "Camera is not supported by this browser.",
    cameraPermission: "Unable to access the camera. Please allow camera permission in Chrome and try again.",
    cameraNotReady: "Camera is not ready yet. Please wait a moment and try again.",
    captureFailed: "Could not capture the camera image.",
    imageFailed: "Image analysis failed.",
    backendImage: "Unable to analyze the camera image. Make sure the Farmer AI backend is running.",
    ragInfoFailed: "Could not retrieve additional RAG information:",
    backend: "Unable to connect to Farmer AI backend. Please make sure the Flask server is running on port 5000.",
    uploadFailed: "File upload failed",
    uploadUnable: "Unable to upload file",
    fileUpload: "Upload file",
    noFarmingInfo: "The available farming information has been used to prepare this recommendation.",
    unknownPest: "Unknown pest"
  },
  Telugu: {
    copilot: "కోపైలట్",
    technology: "సాంకేతికత",
    rag: "RAG ఇంటెలిజెన్స్",
    sources: "మూలాలు",
    explore: "చూడండి",
    badge: "విశ్వసనీయ మూలాల ఆధారిత వ్యవసాయ మేధస్సు",
    heroTitle1: "తెలివైన వ్యవసాయం.",
    heroTitle2: "మెరుగైన నిర్ణయాలు.",
    heroDescription: "మీ వ్యవసాయ ప్రశ్నలను సహజంగా అడగండి మరియు విశ్వసనీయ వ్యవసాయ సమాచారంపై ఆధారపడిన AI సిఫార్సులను పొందండి.",
    upload: "ఫైల్ అప్లోడ్ చేయండి",
    placeholder: "మీ వ్యవసాయ ప్రశ్నను అడగండి...",
    stopVoice: "వాయిస్ ఇన్‌పుట్ ఆపండి",
    speak: "మీ ప్రశ్నను మాట్లాడండి",
    camera: "పంట లేదా పురుగు ఫోటో తీయండి",
    listening: "వింటోంది...",
    uploading: "ఫైల్ అప్లోడ్ అవుతోంది...",
    hint: "Enter నొక్కి ప్రశ్న అడగండి • Hybrid RAG + AI ద్వారా",
    cropAware: "పంట అవగాహన",
    aiPowered: "AI ఆధారితం",
    grounded: "మూలాధారిత సమాధానాలు",
    intelligenceLayer: "మేధస్సు పొర",
    notJustAI: "కేవలం AI కాదు.",
    agriculturalAI: "వ్యవసాయ AI.",
    aiReasoning: "AI విశ్లేషణ",
    aiReasoningText: "వ్యవసాయ భాష, లక్షణాలు, పంటలు, కాలాలు మరియు సందర్భాన్ని అర్థం చేసుకుంటుంది.",
    hybridRAG: "హైబ్రిడ్ RAG",
    hybridRAGText: "సమాధానం రూపొందించే ముందు అత్యంత సంబంధిత వ్యవసాయ సమాచారాన్ని కనుగొని ప్రాధాన్యత ఇస్తుంది.",
    groundedAnswers: "మూలాధారిత సమాధానాలు",
    groundedAnswersText: "సిఫార్సులు ఊహలపై కాకుండా సేకరించిన సమాచారంపై ఆధారపడి రూపొందించబడతాయి.",
    traceability: "మూలాల గుర్తింపు",
    traceabilityText: "ప్రతి సిఫార్సును దానికి ఆధారమైన మూలం మరియు పేజీ వరకు గుర్తించవచ్చు.",
    back: "Farmer AI కి తిరిగి వెళ్లండి",
    recommendation: "FARMER AI సిఫార్సు",
    answered1: "మీ వ్యవసాయ ప్రశ్నకు",
    answered2: "సమాధానం.",
    problem: "సమస్య / సంక్షిప్త సమాధానం",
    check: "ఏమి పరిశీలించాలి",
    action: "ఏమి చేయాలి",
    precautions: "జాగ్రత్తలు",
    source: "మూలాలు",
    page: "పేజీ",
    agriculturalSource: "వ్యవసాయ జ్ఞాన మూలం",
    noInfo: "నిర్దిష్ట సమాచారం అందుబాటులో లేదు.",
    cameraTitle: "పంట / పురుగు కెమెరా",
    cameraSubtitle: "ప్రభావితమైన మొక్క యొక్క స్పష్టమైన ఫోటో తీయండి",
    cancel: "రద్దు చేయండి",
    analyze: "ఫోటో తీసి విశ్లేషించండి",
    analyzing: "విశ్లేషిస్తోంది...",
    imageAnalysis: "AI చిత్ర విశ్లేషణ",
    pestDetected: "పురుగు గుర్తించబడింది",
    confidence: "నమ్మక స్థాయి",
    confidenceLevel: "నమ్మక స్థాయి",
    topPredictions: "అగ్ర అంచనాలు",
    whatDo: "మీరు ఏమి చేయాలి?",
    warning: "AI చిత్ర విశ్లేషణ ఒక ప్రాథమిక సహాయక సాధనం. పురుగుమందులు ఉపయోగించే ముందు అనిశ్చిత ఫలితాలను స్థానిక వ్యవసాయ నిపుణుడితో నిర్ధారించండి.",
    done: "పూర్తయింది",
    footer: "• Hybrid RAG • మూలాధారిత AI",
    voiceUnsupported: "ఈ బ్రౌజర్‌లో వాయిస్ ఇన్‌పుట్‌కు మద్దతు లేదు. Google Chrome లేదా Microsoft Edge ఉపయోగించండి.",
    micBlocked: "మైక్రోఫోన్ అనుమతి నిరోధించబడింది. Chrome అడ్రస్ బార్‌లోని మైక్రోఫోన్ చిహ్నాన్ని క్లిక్ చేసి localhost:5173 కోసం మైక్రోఫోన్‌ను అనుమతించండి.",
    micCapture: "Chrome మీ మైక్రోఫోన్‌ను యాక్సెస్ చేయలేకపోయింది. మైక్రోఫోన్ కనెక్షన్ మరియు Windows మైక్రోఫోన్ అనుమతులను తనిఖీ చేయండి.",
    speechNetwork: "వాయిస్ గుర్తింపు సేవకు కనెక్ట్ కాలేకపోయింది. ఇంటర్నెట్ కనెక్షన్‌ను తనిఖీ చేసి మళ్లీ ప్రయత్నించండి.",
    voiceStart: "వాయిస్ ఇన్‌పుట్ ప్రారంభించలేకపోయింది. మైక్రోఫోన్‌ను మళ్లీ క్లిక్ చేయండి.",
    voiceInit: "వాయిస్ ఇన్‌పుట్ ప్రారంభించలేకపోయింది. మళ్లీ ప్రయత్నించండి.",
    voiceError: "వాయిస్ ఇన్‌పుట్‌లో లోపం ఏర్పడింది. మళ్లీ ప్రయత్నించండి.",
    cameraUnsupported: "ఈ బ్రౌజర్‌లో కెమెరాకు మద్దతు లేదు.",
    cameraPermission: "కెమెరాను యాక్సెస్ చేయలేకపోయింది. Chromeలో కెమెరా అనుమతిని ఇవ్వండి.",
    cameraNotReady: "కెమెరా ఇంకా సిద్ధంగా లేదు. కొద్దిసేపు వేచి ఉండి మళ్లీ ప్రయత్నించండి.",
    captureFailed: "కెమెరా చిత్రాన్ని తీయలేకపోయింది.",
    imageFailed: "చిత్ర విశ్లేషణ విఫలమైంది.",
    backendImage: "కెమెరా చిత్రాన్ని విశ్లేషించలేకపోయింది. Farmer AI backend నడుస్తుందో నిర్ధారించండి.",
    ragInfoFailed: "అదనపు RAG సమాచారాన్ని పొందలేకపోయింది:",
    backend: "Farmer AI backend కు కనెక్ట్ కాలేకపోయింది. Flask server port 5000లో నడుస్తుందో నిర్ధారించండి.",
    uploadFailed: "ఫైల్ అప్లోడ్ విఫలమైంది",
    uploadUnable: "ఫైల్‌ను అప్లోడ్ చేయలేకపోయింది",
    fileUpload: "ఫైల్ అప్లోడ్ చేయండి",
    noFarmingInfo: "ఈ సిఫార్సును సిద్ధం చేయడానికి అందుబాటులో ఉన్న వ్యవసాయ సమాచారాన్ని ఉపయోగించాము.",
    unknownPest: "తెలియని పురుగు"
  },
  Hindi: {
    copilot: "कोपायलट",
    technology: "तकनीक",
    rag: "RAG इंटेलिजेंस",
    sources: "स्रोत",
    explore: "देखें",
    badge: "विश्वसनीय स्रोतों पर आधारित कृषि बुद्धिमत्ता",
    heroTitle1: "स्मार्ट खेती।",
    heroTitle2: "बेहतर फैसले।",
    heroDescription: "अपने खेती से जुड़े सवाल स्वाभाविक रूप से पूछें और विश्वसनीय कृषि ज्ञान पर आधारित AI सुझाव प्राप्त करें।",
    upload: "फ़ाइल अपलोड करें",
    placeholder: "अपनी खेती के बारे में सवाल पूछें...",
    stopVoice: "वॉइस इनपुट रोकें",
    speak: "अपना सवाल बोलें",
    camera: "फसल या कीट की फोटो लें",
    listening: "सुन रहा है...",
    uploading: "फ़ाइल अपलोड हो रही है...",
    hint: "Enter दबाकर सवाल पूछें • Hybrid RAG + AI द्वारा",
    cropAware: "फसल जागरूक",
    aiPowered: "AI आधारित",
    grounded: "स्रोत आधारित",
    intelligenceLayer: "इंटेलिजेंस लेयर",
    notJustAI: "सिर्फ AI नहीं।",
    agriculturalAI: "कृषि AI।",
    aiReasoning: "AI तर्क",
    aiReasoningText: "खेती की भाषा, लक्षणों, फसलों, मौसम और संदर्भ को समझता है।",
    hybridRAG: "हाइब्रिड RAG",
    hybridRAGText: "उत्तर बनाने से पहले सबसे प्रासंगिक कृषि ज्ञान को खोजता और प्राथमिकता देता है।",
    groundedAnswers: "स्रोत आधारित उत्तर",
    groundedAnswersText: "सुझाव अनुमान पर नहीं बल्कि प्राप्त कृषि ज्ञान पर आधारित होते हैं।",
    traceability: "स्रोत ट्रेसबिलिटी",
    traceabilityText: "हर सुझाव को उसके संबंधित स्रोत और पेज तक ट्रेस किया जा सकता है।",
    back: "Farmer AI पर वापस जाएं",
    recommendation: "FARMER AI सुझाव",
    answered1: "आपके खेती के सवाल का",
    answered2: "जवाब।",
    problem: "समस्या / संक्षिप्त उत्तर",
    check: "क्या जांचें",
    action: "क्या करें",
    precautions: "सावधानियां",
    source: "स्रोत",
    page: "पेज",
    agriculturalSource: "कृषि ज्ञान स्रोत",
    noInfo: "कोई विशेष जानकारी उपलब्ध नहीं है।",
    cameraTitle: "फसल / कीट कैमरा",
    cameraSubtitle: "प्रभावित पौधे की साफ फोटो लें",
    cancel: "रद्द करें",
    analyze: "फोटो लें और विश्लेषण करें",
    analyzing: "विश्लेषण हो रहा है...",
    imageAnalysis: "AI IMAGE ANALYSIS",
    pestDetected: "कीट का पता चला",
    confidence: "विश्वास स्तर",
    confidenceLevel: "विश्वास स्तर",
    topPredictions: "शीर्ष अनुमान",
    whatDo: "आपको क्या करना चाहिए?",
    warning: "AI इमेज विश्लेषण एक सहायक जांच उपकरण है। कीटनाशक लगाने से पहले अनिश्चित परिणामों की स्थानीय कृषि विशेषज्ञ से पुष्टि करें।",
    done: "हो गया",
    footer: "• Hybrid RAG • स्रोत आधारित AI",
    voiceUnsupported: "इस ब्राउज़र में वॉइस इनपुट उपलब्ध नहीं है। Google Chrome या Microsoft Edge का उपयोग करें।",
    micBlocked: "माइक्रोफ़ोन की अनुमति बंद है। Chrome के एड्रेस बार में माइक्रोफ़ोन आइकन पर क्लिक करके localhost:5173 के लिए माइक्रोफ़ोन की अनुमति दें।",
    micCapture: "Chrome आपके माइक्रोफ़ोन को एक्सेस नहीं कर सका। माइक्रोफ़ोन कनेक्शन और Windows माइक्रोफ़ोन अनुमति जांचें।",
    speechNetwork: "वॉइस पहचान सेवा से कनेक्ट नहीं हो सका। इंटरनेट कनेक्शन जांचें और फिर प्रयास करें।",
    voiceStart: "वॉइस इनपुट शुरू नहीं हो सका। माइक्रोफ़ोन पर फिर क्लिक करें।",
    voiceInit: "वॉइस इनपुट शुरू नहीं हो सका। फिर प्रयास करें।",
    voiceError: "वॉइस इनपुट में त्रुटि हुई। फिर प्रयास करें।",
    cameraUnsupported: "इस ब्राउज़र में कैमरा उपलब्ध नहीं है।",
    cameraPermission: "कैमरे को एक्सेस नहीं कर सके। Chrome में कैमरा अनुमति दें और फिर प्रयास करें।",
    cameraNotReady: "कैमरा अभी तैयार नहीं है। कुछ क्षण प्रतीक्षा करके फिर प्रयास करें।",
    captureFailed: "कैमरा इमेज कैप्चर नहीं हो सकी।",
    imageFailed: "इमेज विश्लेषण विफल हुआ।",
    backendImage: "कैमरा इमेज का विश्लेषण नहीं हो सका। सुनिश्चित करें कि Farmer AI backend चल रहा है।",
    ragInfoFailed: "अतिरिक्त RAG जानकारी प्राप्त नहीं हो सकी:",
    backend: "Farmer AI backend से कनेक्ट नहीं हो सका। सुनिश्चित करें कि Flask server port 5000 पर चल रहा है।",
    uploadFailed: "फ़ाइल अपलोड विफल हुआ",
    uploadUnable: "फ़ाइल अपलोड नहीं हो सकी",
    fileUpload: "फ़ाइल अपलोड करें",
    noFarmingInfo: "इस सुझाव को तैयार करने के लिए उपलब्ध कृषि जानकारी का उपयोग किया गया है।",
    unknownPest: "अज्ञात कीट"
  }
};

function ui(language, key) {
  return UI_TEXT[language]?.[key] ?? UI_TEXT.English[key] ?? key;
}

/* =========================================================
   3D FARM BACKGROUND
========================================================= */

function FarmVisual() {
  const plants = Array.from({ length: 42 }, (_, i) => i);

  return (
    <div className="farm-visual">
      <div className="sky-glow" />

      <motion.div
        className="sun"
        animate={{
          y: [0, -10, 0],
          scale: [1, 1.04, 1],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <motion.div
        className="cloud cloud-one"
        animate={{ x: [0, 35, 0] }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <motion.div
        className="cloud cloud-two"
        animate={{ x: [0, -25, 0] }}
        transition={{
          duration: 22,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <div className="hill hill-back" />
      <div className="hill hill-front" />

      <div className="farm-ground">
        <div className="farm-path" />

        <motion.div
          className="tractor-3d"
          animate={{
            x: [-18, 18, -18],
            y: [0, -3, 0],
            rotateY: [-3, 3, -3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <div className="tractor-body">
            <div className="tractor-cabin">
              <span />
            </div>

            <div className="tractor-hood" />
            <div className="tractor-exhaust" />

            <div className="tractor-wheel tractor-wheel-back" />
            <div className="tractor-wheel tractor-wheel-front" />
          </div>
        </motion.div>

        <div className="crop-grid">
          {plants.map((plant) => (
            <motion.div
              className="plant"
              key={plant}
              animate={{
                rotate: [-2, 2, -2],
              }}
              transition={{
                duration: 2.5 + (plant % 5) * 0.2,
                repeat: Infinity,
                ease: "easeInOut",
                delay: (plant % 7) * 0.12,
              }}
            >
              <div className="stem" />
              <div className="leaf leaf-left" />
              <div className="leaf leaf-right" />
              <div className="leaf leaf-top" />
            </motion.div>
          ))}
        </div>
      </div>

      <motion.div
        className="farm-particle particle-one"
        animate={{
          y: [0, -35, 0],
          opacity: [0.2, 0.8, 0.2],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
        }}
      />

      <motion.div
        className="farm-particle particle-two"
        animate={{
          y: [0, -45, 0],
          opacity: [0.2, 0.7, 0.2],
        }}
        transition={{
          duration: 7,
          repeat: Infinity,
          delay: 1,
        }}
      />

      <motion.div
        className="farm-particle particle-three"
        animate={{
          y: [0, -30, 0],
          opacity: [0.1, 0.8, 0.1],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          delay: 2,
        }}
      />
    </div>
  );
}

/* =========================================================
   ANSWER PARSER
========================================================= */

function parseAnswer(answer, language = "English") {
  const sections = {
    problem: "",
    check: [],
    action: [],
    precautions: [],
    sources: [],
  };

  const lines = (answer || "")
    .replace(/\r/g, "")
    .split("\n");

  const labels = {
    check: [
      "what to check",
      "ఏమి పరిశీలించాలి",
      "क्या जांचें",
    ],
    action: [
      "what to do",
      "ఏమి చేయాలి",
      "क्या करें",
    ],
    precautions: [
      "precaution",
      "precautions",
      "జాగ్రత్తలు",
      "सावधानियां",
    ],
    sources: [
      "sources",
      "మూలాలు",
      "स्रोत",
    ],
  };

  let current = "problem";

  for (let line of lines) {
    line = line.trim();

    if (!line) continue;

    const clean = line
      .replace(/\*/g, "")
      .trim();

    const lower = clean.toLowerCase();

    if (labels.check.some((label) => lower.includes(label.toLowerCase()))) {
      current = "check";
      continue;
    }

    if (labels.action.some((label) => lower.includes(label.toLowerCase()))) {
      current = "action";
      continue;
    }

    if (labels.precautions.some((label) =>
      lower.includes(label.toLowerCase())
    )) {
      current = "precautions";
      continue;
    }

    if (labels.sources.some((label) =>
      lower.includes(label.toLowerCase())
    )) {
      current = "sources";
      continue;
    }

    if (/^\[SOURCE\s*\d+\]/i.test(line)) {
      sections.sources.push(line);
      continue;
    }

    if (
      current === "check" ||
      current === "action" ||
      current === "precautions"
    ) {
      const text = clean
        .replace(/^[-•*]\s*/, "")
        .replace(/\*\*/g, "")
        .trim();

      if (text) {
        sections[current].push(text);
      }

      continue;
    }

    if (current === "problem") {
      const text = clean
        .replace(/\*\*/g, "")
        .trim();

      if (text && !text.startsWith("[SOURCE")) {
        sections.problem +=
          (sections.problem ? " " : "") + text;
      }
    }
  }

  if (!sections.problem) {
    sections.problem =
      ui(language, "noFarmingInfo");
  }

  return sections;
}

/* =========================================================
   ANSWER CARD
========================================================= */

function AnswerCard({
  icon,
  title,
  children,
  className = "",
}) {
  return (
    <motion.div
      className={`answer-card ${className}`}
      initial={{
        opacity: 0,
        y: 30,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        duration: 0.5,
      }}
      whileHover={{
        y: -5,
      }}
    >
      <div className="answer-card-title">
        <div className="answer-icon">
          {icon}
        </div>

        <h3>{title}</h3>
      </div>

      <div className="answer-card-content">
        {children}
      </div>
    </motion.div>
  );
}

/* =========================================================
   BULLET LIST
========================================================= */

function BulletList({ items, language }) {
  if (!items || items.length === 0) {
    return (
      <p className="no-information">
        {ui(language, "noInfo")}
      </p>
    );
  }

  return (
    <ul className="answer-list">
      {items.map((item, index) => (
        <li key={index}>
          <span className="bullet">✓</span>

          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

/* =========================================================
   ANSWER PAGE
========================================================= */

function AnswerPage({
  question,
  answer,
  citations,
  language,
  onBack,
}) {
  const parsed = parseAnswer(answer, language);

  return (
    <main className="answer-page">
      <nav className="answer-navbar">
        <button
          className="back-button"
          onClick={onBack}
        >
          <ArrowLeft size={18} />
          {ui(language, "back")}
        </button>

        <div className="answer-brand">
          <div className="brand-icon">
            <Leaf size={20} />
          </div>

          <div>
            <strong>Farmer AI</strong>

            <span>{ui(language, "copilot")}</span>
          </div>
        </div>

        <div className="language-badge">
          🌐 {language}
        </div>
      </nav>

      <section className="answer-header">
        <div className="answer-header-badge">
          <Sparkles size={15} />
          {ui(language, "recommendation")}
        </div>

        <h1>
          {ui(language, "answered1")}
          <br />
          <span>{ui(language, "answered2")}</span>
        </h1>

        <div className="question-display">
          <Sparkles size={19} />

          <span>{question}</span>
        </div>
      </section>

      <section className="answer-container">
        <AnswerCard
          icon={<AlertTriangle size={22} />}
          title={ui(language, "problem")}
          className="problem-card"
        >
          <p className="problem-text">
            {parsed.problem}
          </p>
        </AnswerCard>

        <AnswerCard
          icon={<Search size={22} />}
          title={ui(language, "check")}
        >
          <BulletList items={parsed.check} language={language} />
        </AnswerCard>

        <AnswerCard
          icon={<CheckCircle2 size={22} />}
          title={ui(language, "action")}
          className="action-card"
        >
          <BulletList items={parsed.action} language={language} />
        </AnswerCard>

        <AnswerCard
          icon={<ShieldCheck size={22} />}
          title={ui(language, "precautions")}
          className="precaution-card"
        >
          <BulletList items={parsed.precautions} language={language} />
        </AnswerCard>

        <AnswerCard
          icon={<BookOpen size={22} />}
          title={ui(language, "source")}
          className="sources-card"
        >
          {citations && citations.length > 0 ? (
            <div className="source-list">
              {citations.map((citation, index) => (
                <div
                  className="source-item"
                  key={index}
                >
                  <div className="source-number">
                    {citation.id || index + 1}
                  </div>

                  <div>
                    <strong>
                      {citation.source ||
                        ui(language, "agriculturalSource")}
                    </strong>

                    {citation.page && (
                      <span>
                        {ui(language, "page")} {citation.page}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="source-list">
              {parsed.sources.map(
                (source, index) => (
                  <div
                    className="source-item"
                    key={index}
                  >
                    <div className="source-number">
                      {index + 1}
                    </div>

                    <div>{source}</div>
                  </div>
                )
              )}
            </div>
          )}
        </AnswerCard>
      </section>

      <footer className="answer-footer">
        <Leaf size={18} />

        Farmer AI {ui(language, "copilot")}

        <span>
          {ui(language, "footer")}
        </span>
      </footer>
    </main>
  );
}

/* =========================================================
   SPEECH RECOGNITION
========================================================= */

function getSpeechRecognition() {
  return (
    window.SpeechRecognition ||
    window.webkitSpeechRecognition ||
    null
  );
}

/* =========================================================
   TEXT TO SPEECH
========================================================= */

function speakText(text, language) {
  if (!("speechSynthesis" in window)) {
    return;
  }

  window.speechSynthesis.cancel();

  const cleanText = String(text || "")
    .replace(/\[SOURCE\s*\d+\]/gi, "")
    .replace(/\*\*/g, "")
    .trim();

  if (!cleanText) {
    return;
  }

  const utterance =
    new SpeechSynthesisUtterance(cleanText);

  if (language === "Telugu") {
    utterance.lang = "te-IN";
  } else if (language === "Hindi") {
    utterance.lang = "hi-IN";
  } else {
    utterance.lang = "en-IN";
  }

  utterance.rate = 0.9;
  utterance.pitch = 1;

  window.speechSynthesis.speak(utterance);
}

function localizedConfidenceLevel(level, language) {
  const value = String(level || "").toLowerCase();

  if (language === "Telugu") {
    if (value === "high") return "అధిక";
    if (value === "medium") return "మధ్యస్థ";
    if (value === "low") return "తక్కువ";
  }

  if (language === "Hindi") {
    if (value === "high") return "उच्च";
    if (value === "medium") return "मध्यम";
    if (value === "low") return "कम";
  }

  return level || "";
}

/* =========================================================
   HOME
========================================================= */

export default function App() {
  const [question, setQuestion] =
    useState("");

  const [language, setLanguage] =
    useState("English");

  const [loading, setLoading] =
    useState(false);

  const [result, setResult] =
    useState(null);

  useEffect(() => {
    document.documentElement.lang =
      language === "Telugu"
        ? "te"
        : language === "Hindi"
          ? "hi"
          : "en";
  }, [language]);

  const [uploading, setUploading] =
    useState(false);

  const [uploadedFile, setUploadedFile] =
    useState(null);

  const [cameraOpen, setCameraOpen] =
    useState(false);

  const [cameraStream, setCameraStream] =
    useState(null);

  const [cameraBusy, setCameraBusy] =
    useState(false);

  const [cameraResult, setCameraResult] =
    useState(null);

  const cameraVideoRef =
    useRef(null);

  const cameraCanvasRef =
    useRef(null);

  const [listening, setListening] =
    useState(false);

  const recognitionRef =
    useRef(null);

  /* =======================================================
     CAMERA
  ======================================================= */

  async function openCamera() {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert(ui(language, "cameraUnsupported"));
      return;
    }

    try {
      setCameraResult(null);

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: "environment" },
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });

      setCameraStream(stream);
      setCameraOpen(true);

      setTimeout(() => {
        if (cameraVideoRef.current) {
          cameraVideoRef.current.srcObject = stream;
          cameraVideoRef.current.play().catch(() => {});
        }
      }, 100);
    } catch (error) {
      console.error("Camera error:", error);
      alert(
        ui(language, "cameraPermission")
      );
    }
  }

  function closeCamera() {
    if (cameraStream) {
      cameraStream.getTracks().forEach((track) => track.stop());
    }

    if (cameraVideoRef.current) {
      cameraVideoRef.current.srcObject = null;
    }

    setCameraStream(null);
    setCameraOpen(false);
    setCameraBusy(false);
  }

  async function captureCameraImage() {
    if (!cameraVideoRef.current || !cameraCanvasRef.current) {
      return;
    }

    const video = cameraVideoRef.current;
    const canvas = cameraCanvasRef.current;

    if (!video.videoWidth || !video.videoHeight) {
      alert(ui(language, "cameraNotReady"));
      return;
    }

    setCameraBusy(true);

    try {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg", 0.9)
      );

      if (!blob) {
        throw new Error(ui(language, "captureFailed"));
      }

      const formData = new FormData();
      formData.append("file", blob, "farmer-camera.jpg");

      const response = await fetch(
        "https://farmer-ai-backend-4gfg.onrender.com/api/analyze-image",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || ui(language, "imageFailed")
        );
      }

      const pest =
        data.prediction?.pest || ui(language, "unknownPest");

      let knowledge = null;

      try {
        const infoResponse = await fetch(
          "https://farmer-ai-backend-4gfg.onrender.com/api/ask",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              question:
                `The image analysis predicted "${pest}". Explain what this pest is, how a farmer can verify it, what precautions to take, what control measures are recommended, and provide the available agricultural sources.`,
              language,
            }),
          }
        );

        const infoData = await infoResponse.json();

        if (infoResponse.ok) {
          knowledge = infoData;
        }
      } catch (error) {
        console.warn(
          "Could not retrieve additional RAG information:",
          error
        );
      }

      setCameraResult({
        prediction: data.prediction,
        topPredictions: data.top_predictions || [],
        confidenceLevel: data.confidence_level || "Low",
        knowledge,
      });

      closeCamera();
    } catch (error) {
      console.error("Camera analysis error:", error);
      alert(
        error.message ||
          ui(language, "backendImage")
      );
      setCameraBusy(false);
    }
  }

  /* =======================================================
     CLEANUP
  ======================================================= */

  useEffect(() => {
    return () => {
      try {
        recognitionRef.current?.abort();
      } catch (error) {
        console.log(
          "Speech cleanup:",
          error
        );
      }

      if (
        "speechSynthesis" in window
      ) {
        window.speechSynthesis.cancel();
      }

      if (cameraStream) {
        cameraStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [cameraStream]);

  /* =======================================================
     ASK FARMER AI
  ======================================================= */

  async function askFarmerAI() {
    if (!question.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "https://farmer-ai-backend-4gfg.onrender.com/api/ask",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            question:
              question.trim(),

            language,
          }),
        }
      );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Unable to get answer"
        );
      }

      const answer =
        data.answer || "";

      setResult({
        question:
          question.trim(),

        answer,

        citations:
          data.citations || [],

        language,
      });

      /*
       * Read answer aloud.
       *
       * This supports:
       * English
       * Telugu
       * Hindi
       */
      setTimeout(() => {
        speakText(
          answer,
          language
        );
      }, 300);

    } catch (error) {
      console.error(error);

      setResult({
        question:
          question.trim(),

        answer:
          ui(language, "backend"),

        citations: [],

        language,
      });
    } finally {
      setLoading(false);
    }
  }

  /* =======================================================
     FILE UPLOAD
  ======================================================= */

  async function handleFileUpload(e) {
    const file =
      e.target.files?.[0];

    if (!file) {
      return;
    }

    setUploading(true);

    try {
      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      const response =
        await fetch(
          "https://farmer-ai-backend-4gfg.onrender.com/api/upload",
          {
            method: "POST",
            body: formData,
          }
        );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            ui(language, "uploadFailed")
        );
      }

      setUploadedFile(data);

      console.log(
        "Uploaded file:",
        data
      );

    } catch (error) {
      console.error(
        "Upload error:",
        error
      );

      alert(
        error.message ||
          ui(language, "uploadUnable")
      );

    } finally {
      setUploading(false);

      e.target.value = "";
    }
  }

  /* =======================================================
     VOICE INPUT
  ======================================================= */

  function toggleVoiceInput() {
    const Recognition =
      getSpeechRecognition();

    if (!Recognition) {
      alert(
        ui(language, "voiceUnsupported")
      );

      return;
    }

    /*
     * If currently listening,
     * stop the microphone.
     */

    if (listening) {
      try {
        recognitionRef.current?.stop();
      } catch (error) {
        console.log(
          "Stopping voice:",
          error
        );
      }

      setListening(false);

      return;
    }

    /*
     * Remove any old recognition
     * instance before starting a new one.
     */

    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch (error) {
        console.log(
          "Cleaning old recognition:",
          error
        );
      }

      recognitionRef.current = null;
    }

    try {
      const recognition =
        new Recognition();

      /*
       * Language selection
       */

      if (language === "Telugu") {
        recognition.lang =
          "te-IN";
      } else if (
        language === "Hindi"
      ) {
        recognition.lang =
          "hi-IN";
      } else {
        recognition.lang =
          "en-IN";
      }

      recognition.continuous =
        false;

      recognition.interimResults =
        false;

      recognition.maxAlternatives =
        1;

      /* -----------------------------------
         START
      ----------------------------------- */

      recognition.onstart = () => {
        console.log(
          "🎤 Voice recognition started:",
          recognition.lang
        );

        setListening(true);
      };

      /* -----------------------------------
         RESULT
      ----------------------------------- */

      recognition.onresult = (
        event
      ) => {
        try {
          const transcript =
            event.results?.[0]?.[0]
              ?.transcript
              ?.trim() || "";

          console.log(
            "🎤 Recognized:",
            transcript
          );

          if (transcript) {
            setQuestion(
              (previous) =>
                previous
                  ? `${previous} ${transcript}`
                  : transcript
            );
          }
        } catch (error) {
          console.error(
            "Voice result error:",
            error
          );
        }
      };

      /* -----------------------------------
         ERROR
      ----------------------------------- */

      recognition.onerror = (
        event
      ) => {
        console.error(
          "🎤 Speech recognition error:",
          event.error
        );

        setListening(false);

        if (
          event.error ===
          "not-allowed"
        ) {
          alert(
            ui(language, "micBlocked")
          );
        }

        else if (
          event.error ===
          "audio-capture"
        ) {
          alert(
            ui(language, "micCapture")
          );
        }

        else if (
          event.error ===
          "network"
        ) {
          alert(
            ui(language, "speechNetwork")
          );
        }

        else if (
          event.error ===
          "no-speech"
        ) {
          console.log(
            "🎤 No speech detected."
          );
        }

        else if (
          event.error !==
          "aborted"
        ) {
          alert(
            `Voice input error: ${event.error}`
          );
        }
      };

      /* -----------------------------------
         END
      ----------------------------------- */

      recognition.onend = () => {
        console.log(
          "🎤 Voice recognition ended"
        );

        setListening(false);

        if (
          recognitionRef.current ===
          recognition
        ) {
          recognitionRef.current =
            null;
        }
      };

      recognitionRef.current =
        recognition;

      /*
       * Chrome can throw an error if
       * start() happens immediately after
       * another recognition instance ended.
       *
       * Small delay prevents that.
       */

      setTimeout(() => {
        try {
          recognition.start();

        } catch (error) {
          console.error(
            "🎤 Could not start:",
            error
          );

          setListening(false);

          recognitionRef.current =
            null;

          if (
            error.name !==
            "InvalidStateError"
          ) {
            alert(
              ui(language, "voiceStart")
            );
          }
        }
      }, 150);

    } catch (error) {
      console.error(
        "🎤 Voice initialization error:",
        error
      );

      setListening(false);

      recognitionRef.current =
        null;

      alert(
        ui(language, "voiceInit")
      );
    }
  }

  /* =======================================================
     KEYBOARD
  ======================================================= */

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      e.preventDefault();

      askFarmerAI();
    }
  }

  /* =======================================================
     SHOW ANSWER
  ======================================================= */

  if (result) {
    return (
      <main className="app answer-app">

        <FarmVisual />

        <AnswerPage
          question={result.question}
          answer={result.answer}
          citations={result.citations}
          language={result.language}
          onBack={() => {
            if ("speechSynthesis" in window) {
              window.speechSynthesis.cancel();
            }

            setResult(null);
          }}
        />

      </main>
    );
  }

  /* =======================================================
     HOME PAGE
  ======================================================= */

  return (
    <main className="app">

      <FarmVisual />

      <div className="scene-overlay" />

      {/* NAVBAR */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-icon">
            <Leaf size={21} />
          </div>

          <div>
            <strong>
              Farmer AI
            </strong>

            <span>
              Copilot
            </span>
          </div>

        </div>

        <div className="nav-links">

          <a href="#technology">
            {ui(language, "technology")}
          </a>

          <a href="#technology">
            {ui(language, "rag")}
          </a>

          <a href="#technology">
            {ui(language, "sources")}
          </a>

        </div>

        {/* LANGUAGE */}

        <select
          className="language-select"
          value={language}
          onChange={(e) => {
            setLanguage(
              e.target.value
            );
          }}
        >
          <option value="English">
            English
          </option>

          <option value="Telugu">
            తెలుగు
          </option>

          <option value="Hindi">
            हिन्दी
          </option>
        </select>

        <button
          className="nav-button"
          onClick={() => {
            document
              .getElementById(
                "technology"
              )
              ?.scrollIntoView({
                behavior:
                  "smooth",
              });
          }}
        >
          {ui(language, "explore")}

          <ArrowUpRight
            size={16}
          />
        </button>

      </nav>

      {/* HERO */}

      <section className="hero">

        <motion.div
          className="hero-badge"
          initial={{
            opacity: 0,
            y: 20,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.8,
          }}
        >
          <Sparkles size={15} />

          {ui(language, "badge")}

        </motion.div>

        <motion.h1
          initial={{
            opacity: 0,
            y: 45,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 1,
          }}
        >
          {ui(language, "heroTitle1")}

          <br />

          <span>
            {ui(language, "heroTitle2")}
          </span>

        </motion.h1>

        <motion.p
          initial={{
            opacity: 0,
            y: 25,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            delay: 0.25,
            duration: 0.8,
          }}
        >
          {ui(language, "heroDescription")}
        </motion.p>

        {/* QUESTION BOX */}

        <motion.div
          className="question-box"
          initial={{
            opacity: 0,
            scale: 0.94,
          }}
          animate={{
            opacity: 1,
            scale: 1,
          }}
          transition={{
            delay: 0.4,
            duration: 0.7,
          }}
          whileHover={{
            scale: 1.015,
          }}
        >

          <div className="question-icon">
            <Sparkles size={20} />
          </div>

          {/* FILE UPLOAD */}

          <label
            className="upload-button"
            title={ui(language, "upload")}
          >
            <Paperclip size={19} />

            <input
              type="file"
              hidden
              accept=".jpg,.jpeg,.png,.pdf,.txt,.csv,.xlsx"
              onChange={
                handleFileUpload
              }
              disabled={uploading}
            />
          </label>

          {/* QUESTION */}

          <input
            value={question}
            onChange={(e) =>
              setQuestion(
                e.target.value
              )
            }
            onKeyDown={
              handleKeyDown
            }
            placeholder={ui(language, "placeholder")}
            disabled={loading}
          />

          {/* VOICE BUTTON */}

          <button
            type="button"
            className={`voice-button ${
              listening
                ? "voice-listening"
                : ""
            }`}
            onClick={
              toggleVoiceInput
            }
            disabled={loading}
            title={
              listening
                ? ui(language, "stopVoice")
                : ui(language, "speak")
            }
          >
            {listening ? (
              <MicOff size={20} />
            ) : (
              <Mic size={20} />
            )}
          </button>

          {/* CAMERA BUTTON */}

          <button
            type="button"
            className="voice-button camera-button"
            onClick={openCamera}
            disabled={loading || uploading || cameraBusy}
            title={ui(language, "camera")}
          >
            <Camera size={20} />
          </button>

          {/* ASK BUTTON */}

          <motion.button
            onClick={
              askFarmerAI
            }
            disabled={
              loading ||
              !question.trim()
            }
            whileHover={{
              scale: 1.08,
              rotate: -3,
            }}
            whileTap={{
              scale: 0.92,
            }}
          >
            {loading ? (
              "..."
            ) : (
              <ArrowUpRight
                size={22}
              />
            )}
          </motion.button>

        </motion.div>

        {/* VOICE STATUS */}

        {listening && (
          <div className="upload-status">
            🎤 {ui(language, "listening")}
          </div>
        )}

        {/* UPLOAD STATUS */}

        {uploading && (
          <div className="upload-status">
            {ui(language, "uploading")}
          </div>
        )}

        {uploadedFile &&
          !uploading && (
            <div className="upload-status">
              📎{" "}
              {uploadedFile.filename}
            </div>
          )}

        <div className="hint">
          {ui(language, "hint")}
        </div>

        {/* TRUST */}

        <div className="trust-row">

          <div>
            <Leaf />

            <span>
              {ui(language, "cropAware")}
            </span>
          </div>

          <div>
            <Sparkles />

            <span>
              {ui(language, "aiPowered")}
            </span>
          </div>

          <div>
            <ShieldCheck />

            <span>
              {ui(language, "grounded")}
            </span>
          </div>

        </div>

      </section>

      {/* TECHNOLOGY */}

      <section
        className="features"
        id="technology"
      >

        <div className="section-heading">

          <span>
            {ui(language, "intelligenceLayer")}
          </span>

          <h2>
            {ui(language, "notJustAI")}
            <br />
            {ui(language, "agriculturalAI")}
          </h2>

        </div>

        <div className="feature-grid">

          <Feature
            number="01"
            title={ui(language, "aiReasoning")}
            text={ui(language, "aiReasoningText")}
          />

          <Feature
            number="02"
            title={ui(language, "hybridRAG")}
            text={ui(language, "hybridRAGText")}
          />

          <Feature
            number="03"
            title={ui(language, "groundedAnswers")}
            text={ui(language, "groundedAnswersText")}
          />

          <Feature
            number="04"
            title={ui(language, "traceability")}
            text={ui(language, "traceabilityText")}
          />

        </div>

      </section>

      {/* CAMERA MODAL */}

      {cameraOpen && (
        <div className="camera-modal">
          <div className="camera-panel">

            <div className="camera-panel-header">
              <div>
                <strong>{ui(language, "cameraTitle")}</strong>
                <span>
                  {ui(language, "cameraSubtitle")}
                </span>
              </div>

              <button
                type="button"
                className="camera-close"
                onClick={closeCamera}
                disabled={cameraBusy}
                aria-label={ui(language, "cancel")}
              >
                ×
              </button>
            </div>

            <div className="camera-preview">
              <video
                ref={cameraVideoRef}
                autoPlay
                playsInline
                muted
              />
              <div className="camera-frame" />
            </div>

            <canvas
              ref={cameraCanvasRef}
              style={{ display: "none" }}
            />

            <div className="camera-actions">
              <button
                type="button"
                className="camera-cancel"
                onClick={closeCamera}
                disabled={cameraBusy}
              >
                  {ui(language, "cancel")}
              </button>

              <button
                type="button"
                className="camera-capture"
                onClick={captureCameraImage}
                disabled={cameraBusy}
              >
                <Camera size={19} />
                {cameraBusy
                  ? ui(language, "analyzing")
                  : ui(language, "analyze")}
              </button>
            </div>

          </div>
        </div>
      )}

      {/* CAMERA RESULT */}

      {cameraResult && (
        <div className="camera-result-overlay">
          <div className="camera-result-panel">

            <div className="camera-result-header">
              <div>
                <span className="camera-result-label">
                  {ui(language, "imageAnalysis")}
                </span>
                <h2>
                  {cameraResult.prediction?.pest ||
                    ui(language, "pestDetected")}
                </h2>
              </div>

              <button
                type="button"
                className="camera-close"
                onClick={() => setCameraResult(null)}
                aria-label={ui(language, "done")}
              >
                ×
              </button>
            </div>

            <div className="camera-result-summary">
              <div>
                <span>{ui(language, "confidence")}</span>
                <strong>
                  {Number(
                    cameraResult.prediction?.confidence || 0
                  ).toFixed(2)}%
                </strong>
              </div>

              <div>
                <span>{ui(language, "confidenceLevel")}</span>
                <strong>
                  {localizedConfidenceLevel(
                      cameraResult.confidenceLevel,
                      language
                    )}
                </strong>
              </div>
            </div>

            {cameraResult.topPredictions?.length > 0 && (
              <div className="camera-top-predictions">
                <h3>{ui(language, "topPredictions")}</h3>

                {cameraResult.topPredictions.map(
                  (item, index) => (
                    <div
                      className="camera-prediction"
                      key={index}
                    >
                      <span>
                        {item.pest}
                      </span>
                      <strong>
                        {Number(
                          item.confidence || 0
                        ).toFixed(2)}%
                      </strong>
                    </div>
                  )
                )}
              </div>
            )}

            {cameraResult.knowledge?.answer && (
              <div className="camera-knowledge">
                <h3>{ui(language, "whatDo")}</h3>
                <p>
                  {cameraResult.knowledge.answer}
                </p>
              </div>
            )}

            <div className="camera-warning">
              {ui(language, "warning")}
            </div>

            <button
              type="button"
              className="camera-done"
              onClick={() => setCameraResult(null)}
            >
              {ui(language, "done")}
            </button>

          </div>
        </div>
      )}

      <footer>

        <Leaf size={18} />

        Farmer AI {ui(language, "copilot")}

        <span>
          {ui(language, "footer")}
        </span>

      </footer>

    </main>
  );
}

/* =========================================================
   FEATURE CARD
========================================================= */

function Feature({
  number,
  title,
  text,
}) {
  return (
    <motion.div
      className="feature-card"
      whileHover={{
        y: -12,
        scale: 1.025,
        rotateX: 3,
        rotateY: -3,
      }}
      transition={{
        type: "spring",
        stiffness: 250,
        damping: 18,
      }}
    >

      <span>
        {number}
      </span>

      <h3>
        {title}
      </h3>

      <p>
        {text}
      </p>

      <ArrowUpRight
        size={20}
      />

    </motion.div>
  );
}

