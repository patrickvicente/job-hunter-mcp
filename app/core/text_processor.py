"""
Text processing utilities for job descriptions
"""

import re
from typing import Dict, List, Optional

def clean_job_description(description: str) -> str:
    """
    Clean and normalize job description text.
    
    Args:
        description: Raw job description text
        
    Returns:
        Cleaned and normalized description
    """
    if not description:
        return ""
    
    # Normalize line breaks
    text = description.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove excessive whitespace while preserving structure
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Clean each line
        line = line.strip()
        if line:  # Keep non-empty lines
            # Normalize internal whitespace
            line = re.sub(r'\s+', ' ', line)
            cleaned_lines.append(line)
    
    # Join lines with proper spacing
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Final cleanup
    cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)  # Max 2 consecutive line breaks
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def extract_job_sections(description: str) -> Dict[str, str]:
    """
    Extract common job posting sections from description.
    
    Args:
        description: Cleaned job description
        
    Returns:
        Dictionary with section names and content
    """
    sections = {
        "about": "",
        "requirements": "",
        "responsibilities": "",
        "benefits": "",
        "other": ""
    }
    
    lines = description.split('\n')
    current_section = "other"
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Detect section headers
        if any(keyword in line_lower for keyword in ['about', 'overview', 'company', 'description']):
            current_section = "about"
        elif any(keyword in line_lower for keyword in ['requirement', 'qualification', 'experience', 'to be successful', 'about you']):
            current_section = "requirements"
        elif any(keyword in line_lower for keyword in ['responsibility', 'duty', 'role', 'purpose', 'working']):
            current_section = "responsibilities"
        elif any(keyword in line_lower for keyword in ['benefit', 'perk', 'offer', 'what we offer']):
            current_section = "benefits"
        elif any(keyword in line_lower for keyword in ['next step', 'apply', 'contact']):
            current_section = "other"
        else:
            # Add content to current section
            if line.strip():
                sections[current_section] += line + "\n"
    
    # Clean up sections
    for key in sections:
        sections[key] = sections[key].strip()
    
    return sections

def extract_keywords(description: str) -> List[str]:
    """
    Extract potential keywords from job description.
    
    Args:
        description: Cleaned job description
        
    Returns:
        List of potential keywords
    """
    # Common tech keywords
    tech_keywords = [
        'sql', 'database', 'azure', 'cloud', 'python', 'javascript', 'java',
        'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum', 'devops',
        'api', 'rest', 'microservices', 'machine learning', 'ai', 'data',
        'analytics', 'etl', 'data warehouse', 'bi', 'power bi', 'ssis',
        'ssas', 'ssrs', 'aoag', 'replication'
    ]
    
    # Common job keywords
    job_keywords = [
        'engineer', 'developer', 'analyst', 'manager', 'architect',
        'administrator', 'specialist', 'consultant', 'lead', 'senior',
        'junior', 'entry', 'full-time', 'part-time', 'contract',
        'remote', 'hybrid', 'onsite'
    ]
    
    text_lower = description.lower()
    found_keywords = []
    
    # Check for tech keywords
    for keyword in tech_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    # Check for job keywords
    for keyword in job_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return list(set(found_keywords))  # Remove duplicates

def parse_salary(salary_str: str) -> Dict[str, Optional[int]]:
    """
    Parse salary string into min/max values.
    
    Args:
        salary_str: Salary string (e.g., "$80,000 - $120,000", "$100k", "80k-120k")
        
    Returns:
        Dictionary with salary_min and salary_max
    """
    if not salary_str:
        return {"salary_min": None, "salary_max": None}
    
    # Remove common currency symbols and text
    cleaned = re.sub(r'[$,€£¥]', '', salary_str.lower())
    cleaned = re.sub(r'\s+', '', cleaned)
    
    # Handle "k" suffix (thousands)
    cleaned = re.sub(r'k', '000', cleaned)
    
    # Extract numbers
    numbers = re.findall(r'\d+', cleaned)
    
    if len(numbers) >= 2:
        # Multiple numbers found, assume min-max range
        return {
            "salary_min": int(numbers[0]),
            "salary_max": int(numbers[1])
        }
    elif len(numbers) == 1:
        # Single number found, use as min
        return {
            "salary_min": int(numbers[0]),
            "salary_max": None
        }
    else:
        return {"salary_min": None, "salary_max": None}

def parse_posted_date(date_str: str) -> Optional[str]:
    """
    Parse posted date string into ISO format.
    
    Args:
        date_str: Date string from job posting
        
    Returns:
        ISO formatted date string or None if parsing fails
    """
    if not date_str:
        return None
    
    from datetime import datetime
    
    # Common date formats to try
    date_formats = [
        '%Y-%m-%d',           # 2024-01-15
        '%d/%m/%Y',           # 15/01/2024
        '%m/%d/%Y',           # 01/15/2024
        '%Y-%m-%d %H:%M:%S',  # 2024-01-15 10:30:00
        '%d-%m-%Y',           # 15-01-2024
        '%m-%d-%Y',           # 01-15-2024
        '%B %d, %Y',          # January 15, 2024
        '%b %d, %Y',          # Jan 15, 2024
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str.strip(), fmt)
            return parsed_date.isoformat()
        except ValueError:
            continue
    
    return None

def process_job_description(description: str) -> Dict[str, any]:
    """
    Complete job description processing pipeline.
    
    Args:
        description: Raw job description
        
    Returns:
        Dictionary with processed description data
    """
    # Clean the description
    cleaned_description = clean_job_description(description)
    
    # Extract sections
    sections = extract_job_sections(cleaned_description)
    
    # Extract keywords
    keywords = extract_keywords(cleaned_description)
    
    return {
        "description_clean": cleaned_description,
        "description_structured": sections,
        "keywords": keywords,
        "word_count": len(cleaned_description.split()),
        "line_count": len(cleaned_description.split('\n'))
    } 