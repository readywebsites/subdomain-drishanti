import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import AboutPage, AboutSection

def populate_about_page():
    # Clear existing data
    AboutPage.objects.all().delete()
    print("Cleared existing About Page data.")

    # Create the AboutPage instance
    about_page = AboutPage.objects.create(
        hero_image='about/about.webp',
        hero_quote='“A tradition we never questioned. A thought we could never forget.”'
    )
    print("Created AboutPage instance.")

    # Section 1 Data
    section1_content = """
    <p class="leading-relaxed text-[#6d645b] font-bold italic text-left px-4">DRISHANTI began with a thought that never left me.</p>
    <p>Growing up in a Jain family, Rakshapotli was simply a part of life. Tied around the wrist, it represented blessings, protection, and a personal commitment to ourselves. Like many traditions, it became part of everyday life. And like many traditions, we rarely stopped to ask why.</p>
    <p>Until one simple conversation changed everything.<br /><br />“Why should something so meaningful remain temporary?”<br /><br />Those words came from my late father, <b>Shantilal Popatlal Gada</b>.</p>
    <p>At the time, I was beginning my journey in jewellery design, a path that would eventually span nearly two decades, formal training in Jewellery Design & Manufacture, and recognition through national and international design awards.</p>
    <p>Yet this idea did not begin in a design studio.<br /><br />It began at home.</p>
    <p>Every few months, the Rakshapotli I wore would loosen, wear out, break, or simply fade with time. A new one would replace the old, but the thought never left me.</p>
    <p class="quote">If its meaning could endure for generations, why couldn't its form?</p>
    <p>Harshmi Sheth<br />Founder & Creative Director, DRISHANTI</p>
    """

    # Section 2 Data
    section2_content = """
    <p class="quote">“What began as a simple question gradually became the inspiration behind DRISHANTI.”</p>
    <p>For me, jewellery has never been about ornamentation alone. I have always believed that the pieces we wear should carry meaning, memory, and connection</p>
    <p>Later, after marrying my husband,<b> Vinit Sheth</b>, also a Co-founder of DRISHANTI,  I found someone who shared the same belief. Together, we felt a responsibility to preserve the essence of the Rakshapotli while creating a form that could be treasured for years to come.</p>
    <p>Before creating a single piece, we spent years understanding Rakshapotli beyond its appearance. We learned through conversations with elders, Jain gurus, and Acharya Maharaj Sahebs, seeking to understand its significance, purpose, and place within tradition.</p>
    <p>Only then did we begin.</p>
    <p class="quote">What we create today is not a reinterpretation of a tradition, but an effort to preserve it with the respect it deserves.</p>
    """

    # Section 3 Data
    section3_content = """
    <p>The name <b class="text-[#2c2c2c] font-semibold text-[16px] xl:text-[18px] 2xl:text-[22px]">DRISHANTI</b> comes from <br /> 
    <span class="text-[#2c2c2c] italic text-[16px] xl:text-[18px] 2xl:text-[22px]">दृष्टि + शांति = Drishanti</span>.
    <br />A Vision of Peace. A Vision of DAD.</p>
    <p>It reflects the spirit in which this journey began thoughtful, purposeful, and rooted in meaning.</p>
    <p>More importantly, it is a tribute.<br /><br />A tribute to my father, whose question stayed with me long after the conversation ended. 
    Looking back, I realise it was never simply about preserving a Rakshapotli. It was a vision beyond it.<br /><br />It was about preserving the values, conversations, and memories that we inherit and carry forward.</p>
    <div class="mt-14 pt-8 border-t border-[#e8dccb] flex justify-end relative translate-x-8 xl:translate-x-16 2xl:translate-x-24">
    <p class="quote">“In many ways, <br />DRISHANTI is my. way of continuing that conversation.......”</p>
    </div>
    """

    # Create the sections
    AboutSection.objects.create(
        page=about_page,
        image='about/about1.webp',
        content=section1_content,
        image_position='right',
        display_order=1
    )
    print("Created AboutSection 1.")

    AboutSection.objects.create(
        page=about_page,
        image='about/about2.webp',
        content=section2_content,
        image_position='left',
        display_order=2
    )
    print("Created AboutSection 2.")

    AboutSection.objects.create(
        page=about_page,
        image='about/dad.webp',
        content=section3_content,
        image_position='right',
        display_order=3
    )
    print("Created AboutSection 3.")

    print("About Page population complete.")

if __name__ == '__main__':
    populate_about_page()
