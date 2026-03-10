#!/usr/bin/env python3
"""
Build ADR presentation from Red Hat template

This script creates the complete ADR presentation from scratch:
1. Copies Red Hat Consulting template
2. Removes unnecessary slides
3. Populates content slides
4. Applies formatting (bullets, bold)
5. Adds speaker notes

Usage:
    python scripts/build_presentation.py

Requirements:
    - credentials.json and token.json in parent directory
    - Red Hat template ID: 1B5s3eIrvbW7ZXDX0BH5qKb8b09pYudWyYPJUjw1ruQI
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

TEMPLATE_ID = '1B5s3eIrvbW7ZXDX0BH5qKb8b09pYudWyYPJUjw1ruQI'
NEW_TITLE = 'Architecture Decision Records in Consulting Delivery'

def get_credentials():
    """Get valid credentials, refreshing if needed"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        print("Refreshing expired token...")
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def copy_template(service_drive, title):
    """Copy the Red Hat template"""
    try:
        copied_file = service_drive.files().copy(
            fileId=TEMPLATE_ID,
            body={'name': title}
        ).execute()

        presentation_id = copied_file.get('id')
        print(f"✅ Created presentation: {presentation_id}")
        return presentation_id
    except HttpError as error:
        print(f"❌ Error copying template: {error}")
        sys.exit(1)

def delete_slides(service, presentation_id, slide_indices):
    """Delete slides by index (0-based)"""
    try:
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        slide_ids = [slides[i].get('objectId') for i in slide_indices if i < len(slides)]

        if not slide_ids:
            return

        requests = [{'deleteObject': {'objectId': sid}} for sid in slide_ids]

        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        print(f"✅ Deleted {len(slide_ids)} slides")
    except HttpError as error:
        print(f"❌ Error deleting slides: {error}")
        sys.exit(1)

def get_body_id(presentation, slide_id):
    """Get the BODY text box ID from a slide"""
    for slide in presentation.get('slides', []):
        if slide.get('objectId') == slide_id:
            for element in slide.get('pageElements', []):
                if 'shape' in element:
                    placeholder = element['shape'].get('placeholder', {})
                    if placeholder.get('type') == 'BODY':
                        return element.get('objectId')
    return None

def rebuild_slide_content(service, presentation_id, slide_id, body_id, content_structure):
    """Rebuild slide content with proper formatting"""
    try:
        requests = []

        # Delete existing text
        requests.append({
            'deleteText': {
                'objectId': body_id,
                'textRange': {'type': 'ALL'}
            }
        })

        # Insert new text
        full_text = '\n'.join([item['text'] for item in content_structure])
        requests.append({
            'insertText': {
                'objectId': body_id,
                'text': full_text,
                'insertionIndex': 0
            }
        })

        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        # Apply formatting in three phases
        delete_bullet_requests = []
        format_requests = []
        create_bullet_requests = []
        current_index = 0

        for item in content_structure:
            text_length = len(item['text']) + 1
            end_index = current_index + text_length - 1

            # Phase 1: Delete all bullets
            delete_bullet_requests.append({
                'deleteParagraphBullets': {
                    'objectId': body_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': current_index,
                        'endIndex': end_index
                    }
                }
            })

            # Phase 2: Apply bold if needed
            if item.get('bold', False):
                format_requests.append({
                    'updateTextStyle': {
                        'objectId': body_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': current_index,
                            'endIndex': end_index
                        },
                        'style': {'bold': True},
                        'fields': 'bold'
                    }
                })

            # Phase 3: Re-create bullets for level 1 and 2
            if item['level'] > 0:
                create_bullet_requests.append({
                    'createParagraphBullets': {
                        'objectId': body_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': current_index,
                            'endIndex': end_index
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                })

                indent_pt = 18 if item['level'] == 1 else 54

                format_requests.append({
                    'updateParagraphStyle': {
                        'objectId': body_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': current_index,
                            'endIndex': end_index
                        },
                        'style': {
                            'indentStart': {
                                'magnitude': indent_pt,
                                'unit': 'PT'
                            },
                            'indentFirstLine': {
                                'magnitude': 0,
                                'unit': 'PT'
                            }
                        },
                        'fields': 'indentStart,indentFirstLine'
                    }
                })

            current_index += text_length

        # Execute in order
        if delete_bullet_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': delete_bullet_requests}
            ).execute()

        if format_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': format_requests}
            ).execute()

        if create_bullet_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': create_bullet_requests}
            ).execute()

        return True

    except HttpError as error:
        print(f"❌ Error updating slide: {error}")
        return False

def add_speaker_notes(service, presentation_id, slide_id, notes_text):
    """Add speaker notes to a slide"""
    try:
        presentation = service.presentations().get(presentationId=presentation_id).execute()

        target_slide = None
        for slide in presentation.get('slides', []):
            if slide.get('objectId') == slide_id:
                target_slide = slide
                break

        if not target_slide:
            return False

        notes_page = target_slide.get('slideProperties', {}).get('notesPage', {})
        notes_body_id = None
        has_text = False

        for element in notes_page.get('pageElements', []):
            if 'shape' in element:
                placeholder = element['shape'].get('placeholder', {})
                if placeholder.get('type') == 'BODY':
                    notes_body_id = element.get('objectId')
                    text_content = element.get('shape', {}).get('text', {})
                    text_elements = text_content.get('textElements', [])
                    for te in text_elements:
                        if 'textRun' in te and te['textRun'].get('content', '').strip():
                            has_text = True
                            break
                    break

        if not notes_body_id:
            return False

        requests = []

        if has_text:
            requests.append({
                'deleteText': {
                    'objectId': notes_body_id,
                    'textRange': {'type': 'ALL'}
                }
            })

        requests.append({
            'insertText': {
                'objectId': notes_body_id,
                'text': notes_text,
                'insertionIndex': 0
            }
        })

        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        return True

    except HttpError as error:
        return False

def main():
    """Main function"""
    try:
        print("="*80)
        print("Building ADR Presentation from Template")
        print("="*80)

        # Get credentials
        creds = get_credentials()
        service_slides = build('slides', 'v1', credentials=creds)
        service_drive = build('drive', 'v3', credentials=creds)

        # Copy template
        print("\n1. Copying Red Hat template...")
        presentation_id = copy_template(service_drive, NEW_TITLE)

        # Get presentation structure
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        print(f"   Template has {len(slides)} slides")

        # Delete unnecessary slides (keep slide 0=title, 1=content template, last=closing)
        print("\n2. Removing unnecessary slides...")
        # Keep slides 0, 1, and last slide (130), delete everything else between 2-129
        slides_to_delete = list(range(2, len(slides) - 1))
        delete_slides(service_slides, presentation_id, slides_to_delete)

        # Refresh presentation
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        print(f"   Now has {len(slides)} slides")

        # Duplicate content slide to create 5 content slides (slides 2-6)
        print("\n3. Creating content slides...")
        content_template_id = slides[1].get('objectId')

        requests = []
        for i in range(4):  # Need 4 more copies (already have 1)
            requests.append({
                'duplicateObject': {
                    'objectId': content_template_id
                }
            })

        service_slides.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        # Refresh presentation
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        print(f"   Now has {len(slides)} slides (should be 7)")

        # Define slide content
        slide_contents = {
            1: [  # Slide 2: What Are ADRs?
                {'text': 'Architecture Decision Records (ADRs) document strategic choices between valid architecture alternatives during design phases in our consulting engagement.', 'level': 0, 'bold': False},
                {'text': 'IT IS NOT: Configuration Checklist', 'level': 0, 'bold': True},
                {'text': '"Set parameter X to value Y"', 'level': 1},
                {'text': '"Enable feature Z because it\'s required"', 'level': 1},
                {'text': 'IT IS: REAL Architecture Decisions', 'level': 0, 'bold': True},
                {'text': '"KServe vs. Custom Deployment for model serving?"', 'level': 1},
                {'text': '"Internal PostgreSQL vs. External managed DB?"', 'level': 1},
                {'text': '"Fast channel (early features) vs. Stable (production)?"', 'level': 1},
            ],
            2: [  # Slide 3: ADR Structure
                {'text': 'Each ADR follows a strict format:', 'level': 0, 'bold': False},
                {'text': 'Title: Concise description', 'level': 1, 'bold': True},
                {'text': 'Architectural Question: What choice is being made?', 'level': 1, 'bold': True},
                {'text': 'Issue: Why is this decision needed?', 'level': 1, 'bold': True},
                {'text': 'Assumptions: Dependencies or prerequisites', 'level': 1, 'bold': True},
                {'text': 'Alternatives: 2+ viable options', 'level': 1, 'bold': True},
                {'text': 'Decision: #TODO# until decided', 'level': 1, 'bold': True},
                {'text': 'Justification: Why choose each alternative', 'level': 1, 'bold': True},
                {'text': 'Implications: Consequences, trade-offs, risks', 'level': 1, 'bold': True},
                {'text': 'Agreeing Parties: Customer + Red Hat roles', 'level': 1, 'bold': True},
                {'text': '→ See adr-structure-example.png for real example', 'level': 0, 'bold': False},
            ],
            3: [  # Slide 4: Why ADRs Matter?
                {'text': 'The Problem:', 'level': 0, 'bold': True},
                {'text': 'Workshops happen, decisions captured (Miro/paper)', 'level': 1},
                {'text': 'NOT formalized into design doc ❌', 'level': 1},
                {'text': 'Workshop outputs vanish', 'level': 1},
                {'text': 'Consultants implement without context', 'level': 1},
                {'text': 'The Opportunity:', 'level': 0, 'bold': True},
                {'text': '15-30 min per ADR to formalize workshop outputs', 'level': 1},
                {'text': 'Complete design deliverables with rationale', 'level': 1},
                {'text': 'Smoother handover, reduced disputes', 'level': 1},
                {'text': 'Permanent record for future audits', 'level': 1},
                {'text': 'Note: CER decommissioned, ADRs go in design docs', 'level': 0, 'bold': False},
            ],
            4: [  # Slide 5: Who & When?
                {'text': 'Three Consulting Phases:', 'level': 0, 'bold': True},
                {'text': 'Design (Architect)', 'level': 1},
                {'text': 'Implementation (Consultant)', 'level': 1},
                {'text': 'Enablement (Consultant)', 'level': 1},
                {'text': 'ADR Workflow:', 'level': 0, 'bold': True},
                {'text': 'Preparation: Extract decision points from docs', 'level': 1},
                {'text': 'Workshop: Present questions, capture decisions', 'level': 1},
                {'text': 'Design: Formalize Miro → ADRs in design doc', 'level': 1},
                {'text': 'Handover: Consultant gets full context', 'level': 1},
                {'text': 'Best Practice: Workshop → Miro → ADRs → Diagrams', 'level': 0, 'bold': True},
            ],
            5: [  # Slide 6: Real Example
                {'text': 'OCP-BASE-01: Cluster Isolation Strategy', 'level': 0, 'bold': True},
                {'text': 'Question: How to separate Dev/Test/Prod workloads?', 'level': 0, 'bold': False},
                {'text': 'Alternatives:', 'level': 0, 'bold': True},
                {'text': 'Consolidated (Single Cluster)', 'level': 1},
                {'text': 'Prod/Non-Prod Split', 'level': 1},
                {'text': 'Per-Environment', 'level': 1},
                {'text': 'Decision: Separate by infrastructure type', 'level': 0, 'bold': True},
                {'text': 'OpenStack: General purpose/dev workloads', 'level': 1},
                {'text': 'Bare Metal: Performance/prod with GPUs', 'level': 1},
                {'text': 'Agreeing Parties:', 'level': 0, 'bold': True},
                {'text': 'J. Smith (AI/ML Platform Owner)', 'level': 1},
                {'text': 'A. Johnson (Storage Expert)', 'level': 1},
                {'text': 'M. Chen (Security Expert)', 'level': 1},
            ],
        }

        # Speaker notes
        speaker_notes = {
            0: """Welcome. Today I'll show you why Architecture Decision Records should be part of every design document. This is a 10-minute overview, and I'll demo our ADR repository with 271 documented decisions at the end.""",

            1: """ADRs document strategic architectural choices during design phases - not configuration checklists.

A configuration checklist is "set this parameter to this value" - there's no choice. Real architectural decisions have multiple valid alternatives: KServe vs custom deployment, internal vs external database, fast vs stable update channel.""",

            2: """Every ADR follows the same structure with these fields shown here. Notice each field is bold: Title, Architectural Question, Issue, Assumptions, Alternatives, Decision (starts as #TODO#), Justification, Implications, Agreeing Parties.

The screenshot shows a real example from our RHOAI repository - RHOAI-SM-47 about Model Registry database strategy.""",

            3: """Why do ADRs matter? The problem: Architects already facilitate workshops and capture decisions on Miro boards or paper. But these captures aren't formalized into the design document. Workshop outputs vanish. Consultants implement without understanding why choices were made.

The opportunity: Just 15-30 minutes per ADR to formalize workshop outputs into design documents. This gives complete deliverables with rationale, smoother handover, reduced disputes, and permanent records for future audits.

Note: CER is decommissioned due to the Tang project. ADRs now go directly in design documents.""",

            4: """Who creates ADRs and when? Consulting delivery has three phases: Design by Architects, Implementation by Consultants, Enablement by Consultants.

The ADR workflow: Preparation - extract decision points from Red Hat docs. Workshop - present questions, capture decisions on Miro or paper. Design phase - formalize those Miro captures into ADRs in the design document. Handover - consultant receives full context.

Best practice flow: Workshop to Miro to ADRs to Diagrams. This ensures nothing is lost.""",

            5: """Real example showing the complete ADR structure. OCP-BASE-01: Cluster Isolation Strategy. The question was how to separate Dev, Test, and Prod workloads across OpenShift clusters.

Three alternatives were considered: Consolidated single cluster, Prod/Non-Prod split, or per-environment separation.

The decision: Separate clusters based on infrastructure type. OpenStack hosts general purpose and dev workloads. Bare Metal hosts performance-intensive production workloads with GPUs.

Agreeing parties included the AI/ML Platform Owner, Storage Expert, and Security Expert. Names obfuscated here for demo purposes.""",
        }

        # Populate content slides
        print("\n4. Populating content slides...")
        for slide_idx, content in slide_contents.items():
            slide = slides[slide_idx]
            slide_id = slide.get('objectId')
            body_id = get_body_id(presentation, slide_id)

            if body_id:
                print(f"   Slide {slide_idx + 1}: Updating content...")
                if rebuild_slide_content(service_slides, presentation_id, slide_id, body_id, content):
                    print(f"   Slide {slide_idx + 1}: ✅ Content updated")

                    # Add speaker notes
                    if slide_idx in speaker_notes:
                        if add_speaker_notes(service_slides, presentation_id, slide_id, speaker_notes[slide_idx]):
                            print(f"   Slide {slide_idx + 1}: ✅ Speaker notes added")

        print("\n" + "="*80)
        print("✅ Presentation built successfully")
        print("="*80)
        print(f"\n🔗 View: https://docs.google.com/presentation/d/{presentation_id}/edit")
        print(f"\nPresentation ID: {presentation_id}")
        print("\n📊 Structure (7 slides):")
        print("   Slide 1: Title")
        print("   Slide 2: What Are ADRs?")
        print("   Slide 3: ADR Structure")
        print("   Slide 4: Why ADRs Matter?")
        print("   Slide 5: Who & When?")
        print("   Slide 6: Real Example")
        print("   Slide 7: Closing")
        print("\n💡 Note: Add screenshot manually to Slide 3")
        print("   File: adr-structure-example.png")

    except HttpError as error:
        print(f"❌ An error occurred: {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
