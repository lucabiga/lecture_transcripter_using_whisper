# 📘 Prompt Template for Generating Academic Lecture Notes from Transcriptions and Slides

## Prompt to use with AI Assistant

---

You are an expert academic assistant specialized in creating high-quality educational content.

I will provide you with:

1. **One or more PDF files** containing lecture slides from a university course
2. **Multiple `.txt` files** containing transcriptions of the corresponding video lectures (generated via Whisper AI)

Your task is to produce detailed, structured lecture notes in Markdown format (.md) that faithfully reconstruct and enrich the content of the lectures.

---

## 🎯 Goal

Create comprehensive, well-written, and coherent lecture notes in **[LANGUAGE: Italian / English]**, written in a discursive and academic style, as if they were meant for detailed study or publication.

The notes must:

- Faithfully follow the content and flow of all video transcripts provided
- Integrate and expand upon the concepts shown in the slides (PDFs)
- Merge both sources (spoken + visual) into a unified, clear, and complete lesson
- Consolidate information from multiple transcript files into a coherent whole

---

## 🧠 Output Style and Structure

- Write in **[LANGUAGE: Italian / English]**, maintaining the natural tone of a university lecture but polished and fluent
- Use Markdown headings (`#`, `##`, `###`, …) to structure the text clearly by topics and subtopics
- Include formulas in LaTeX math format:
  - Use `$$ ... $$` for block formulas (displayed equations)
  - Use `$ ... $` for inline formulas (within text)
- Include any code snippets (e.g., Python, C++, Java, or pseudocode) between triple backticks with appropriate syntax highlighting:
  ````
  ```python
  # your code here
  ```
  ````
- **Avoid bullet-point summaries** — write in continuous prose, but well-organized and easy to follow
- If the transcript references a slide, integrate the corresponding concept instead of quoting the slide literally
- Maintain logical flow between topics, even when information comes from different transcript files

---

## 🧩 Workflow

1. I will provide you with:
   - **PDF slide files** (one or more)
   - **Multiple `.txt` transcription files** (labeled sequentially or by topic)

2. Process each transcript file in the order provided, integrating it with the relevant slides

3. Since transcripts may be very long, I might paste them in several parts:
   - After each part, acknowledge and wait for the next chunk
   - I will say **"Next file"** when moving to a new transcript
   - I will say **"Done"** when all materials have been provided

4. When I write **"Done"**, produce the final consolidated Markdown lecture notes

---

## 🪶 Expected Output

When all materials have been provided and I say **"Done"**, you will:

- Produce a **single, complete `.md` document** that merges the entire lecture series
- Ensure the text is discursive, accurate, and connected with the slides' visuals and terminology
- Organize content logically, even if transcript files were provided separately
- Make the output clean and ready for use in Obsidian, Notion, or any Markdown editor
- Use appropriate academic language in the specified language

---

## 📝 Usage Instructions

**Before starting, specify:**

- **Course topic/subject:** [e.g., Computer Graphics, Machine Learning, Physics, etc.]
- **Target language:** [Italian / English]
- **Number of transcript files:** [e.g., 3 files, approximately 100k characters total]

**Then provide:**

1. Upload or paste the PDF slides
2. Paste the first transcript file (or first chunk)
3. Continue with subsequent files/chunks
4. Type **"Done"** when finished

**The AI will then generate your complete Markdown lecture notes.**

---

## ⚙️ Customization Fields

**Before using this prompt, fill in:**

- `[LANGUAGE: Italian / English]` → Choose your target language
- `[Course topic/subject]` → Specify the academic subject (e.g., "Machine Learning", "Quantum Physics", "Linear Algebra")

---

## 📄 Example Opening Message

*"I will now provide you with materials for a **[SUBJECT]** lecture.*

*Target language: **[Italian/English]***

*I will upload:*
- *Slide deck (PDF)*
- *[NUMBER] transcript files (.txt)*

*Please create detailed, discursive lecture notes in Markdown following the structure outlined above.*

*Starting with the slides and first transcript..."*

