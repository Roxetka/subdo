import requests
import logging
from telegram import Update
from telegram.ext import CallbackContext, ApplicationBuilder, CommandHandler
import re

# API URL-domen adını dinamik əlavə etmək üçün dəyişdirildi
SUBDOMAIN_API_URL = 'https://subdomains.whoisxmlapi.com/api/v1?apiKey=at_JoyNq3JxdRZxJDmxfeyL53Yq6WsiI&domainName='

def clean_domain(domain):
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    domain = domain.rstrip('/')
    return domain

async def subdomain(update: Update, context: CallbackContext) -> None:
    try:
        command, domain_name = update.message.text.split(' ', 1)
        domain_name = domain_name.strip()

        if domain_name:
            # Domain adını təmizləyin
            domain_name = clean_domain(domain_name)

            await update.message.reply_text('Subdomain sorğulanır, gözləyin...')

            # API sorğusu
            response = requests.get(f"{SUBDOMAIN_API_URL}{domain_name}")
            response_data = response.json()

            # Cavab yoxlanılır
            if 'result' in response_data and 'records' in response_data['result']:
                records = response_data['result']['records']
                if records:
                    message = ""
                    for record in records:
                        message += (
                            f"Subdomain: {record.get('domain')}\n"
                            "---------------------------------------\n"
                        )

                    with open('subdomain.txt', 'w', encoding='utf-8') as f:
                        f.write(message)

                    # Dosyanı göndər
                    with open('subdomain.txt', 'rb') as doc:
                        await context.bot.send_document(update.effective_chat.id, document=doc)

                else:
                    await update.message.reply_text("Bu domain üçün subdomain tapılmadı.")
            else:
                await update.message.reply_text("API cavabında xəta oldu və ya subdomain məlumatı mövcud deyil.")

        else:
            await update.message.reply_text('/subdomain əmrindən düzgün formatda istifadə edin: /subdomain (domain_name)')

    except ValueError:
        await update.message.reply_text('/subdomain əmrindən düzgün formatda istifadə edin: /subdomain (domain_name)')

    except Exception as e:
        logging.error(f"Xəta, /subdomain funksiyasında: {e}")
        await update.message.reply_text("Xəta baş verdi. Zəhmət olmasa daha sonra yenidən yoxlayın.")


if __name__ == '__main__':
    # Bot tokeni əlavə edin
    application = ApplicationBuilder().token('7705392384:AAF_ugqfMOPV601qro-JFXVa2fh9sHvkJSU').build()

    # /subdomain komutu üçün handler əlavə edin
    subdomain_handler = CommandHandler('subdomain', subdomain)
    application.add_handler(subdomain_handler)

    # Botu işə salın
    application.run_polling()