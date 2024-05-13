from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from .forms import CustomAuthenticationForm, CustomerRegistrationForm, AddRecipeForm, EditRecipeForm, ReviewForm
from .models import *
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All
from gpt4all import GPT4All as gpt
import os


chain = None
chat_history = list()

@csrf_exempt  # Only for demonstration. Use CSRF protection in production.
def contact_form_submission(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        message = request.POST.get('Message')

        # Send email
        send_mail(
            'Contact Form Submission',
            f'Email: {email}\nMessage: {message}',
            'recipesa369@gmail.com',  # Replace with your email
            ['dobrinkasotirovapvt@gmail.com'],  # Replace with recipient's email
            fail_silently=False,
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def index(request):
    recipes = Recipe.objects.all()[:6]
    return render(request, "index.html",
                  context={"recipe1": recipes[0], "recipe2": recipes[1], "recipe3": recipes[2], "recipes": recipes})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful registration
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def all_recipes(request):
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "all_recipes.html", context)


def details(request, recipe_id=None):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = Category.objects.all()
    reviews = Review.objects.filter(recipe=recipe).all()
    total_review = 0
    if reviews:
        total = 0
        for review in reviews:
            total += review.rating
        total_review = total / len(reviews) * 1.0
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Review instance, but don't save it to the database yet
            new_review = form.save(commit=False)
            # Now you can set the additional fields on the new_review object
            new_review.recipe = recipe
            new_review.user = request.user
            new_review.date_posted = timezone.now()  # It's better to use Django's timezone.now()
            # Save the new_review instance to the database
            new_review.save()
            return redirect('details', recipe_id=recipe_id)

    context = {
        'recipe': recipe,
        'categories': categories,
        'reviews': reviews,
        'form': form,
        'total_review': round(total_review, 1)
    }
    return render(request, 'details.html', context=context)


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    # Redirect to the book list page or any other appropriate URL
    return redirect('/recipes')


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # Create but don't save yet
            recipe.user = request.user  # Set the user
            recipe.save()  # Save the object with user assigned
            # Redirect to the book details page or any other appropriate URL
            return redirect('/recipes')
    else:
        form = AddRecipeForm()

    return render(request, 'add_recipes.html', {'form': form})


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = EditRecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            if 'image' not in request.FILES:  # No new photo uploaded
                form.fields['image'].required = False
            form.save()
            # Redirect to the book details page or any other appropriate URL
            return redirect('details', recipe_id=recipe_id)
        else:
            print(form.errors)
    else:
        form = EditRecipeForm(instance=recipe)

    return render(request, 'details.html', {'form': form})


def for_you(request):
    return render(request, "for_you.html", context={"chat_history":chat_history})


# def recipe_review(request, recipe_id):
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     reviews = Review.objects.filter(recipe=recipe)
#     form = ReviewForm()
#     if request.method == 'POST':
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.recipe = recipe
#             review.user = request.user
#             review.save()
#             return redirect('details', recipe_id=recipe_id)
#     return render(request, 'details.html', {'recipe': recipe, 'reviews': reviews, 'form': form})

def contact(request):
    return render(request, "contact.html")


def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user).all()
    return render(request, "recipes.html", context={"recipes": recipes})


def gpt4all_recipe_suggestions(request):
    global chain
    if request.method == 'POST':
        question = request.POST.get('question')  # Get the question from the form
        knowledge_base_folder = 'recipes/model_data'
        files = os.listdir(knowledge_base_folder)
        documents = list()
        for f in files:
            try:
                file_path = f"{knowledge_base_folder}/{f}"

                # Assuming TextLoader is used to load text from PDF
                loader = TextLoader(file_path, encoding = 'UTF-8')
                text = loader.load()

                documents.extend(text)
                print(documents)

            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=30)
        split_documents = text_splitter.split_documents(documents)
        print(len(split_documents))
        vectorstore = Chroma.from_documents(documents=split_documents, embedding=GPT4AllEmbeddings())
        print(gpt.list_models())
        llm = GPT4All(model="recipes/model/mistral-7b-openorca.gguf2.Q4_0")
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
        chain = ConversationalRetrievalChain.from_llm(llm, retriever)
        global chat_history
        chat_history = ask_bot(question)  # Assuming ask_bot function exists
        print(chat_history)
        return render(request, "for_you.html", context={"chat_history": chat_history})

    return redirect('/')


def ask_bot(query):
    global chat_history
    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    print(chat_history[-1][1])
    return chat_history

def search(request):
    search_term = request.GET.get('search_term')
    recipes = Recipe.objects.filter(name__icontains=search_term).all()
    context = {"recipes": recipes, "search_term": search_term}
    return render(request, 'all_recipes.html', context)

