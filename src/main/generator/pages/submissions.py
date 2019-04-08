from code.util.db import Submission
from code.generator.lib.htmllib import *
from code.generator.lib.page import *
from code.util import register
from code.generator.pages.judge import verdict_name, icons
import logging

class SubmissionDisplay(UIElement):
    def __init__(self, submission: Submission):
        subTime = submission.timestamp
        probName = submission.problem.title
        cls = "gray" if submission.status == "Review" else "red" if submission.result != "ok" else ""
        self.html = Card("Submission to {} at <span class='time-format'>{}</span>".format(probName, subTime), [
            h.strong("Language: <span class='language-format'>{}</span>".format(submission.language)),
            h.br(),
            h.strong("Result: <span class='result-format'>{}</span>".format(verdict_name[submission.getContestantResult()])),
            h.br(),
            h.br(),
            h.strong("Code:"),
            h.code(submission.code.replace("\n", "<br/>").replace(" ", "&nbsp;"))
        ], cls=cls)

class SubmissionRow(UIElement):
    def __init__(self, sub):
        self.html = h.tr(
            h.td(sub.problem.title),
            h.td(cls='time-format', contents=sub.timestamp),
            h.td(sub.language),
            h.td(
                h.i("&nbsp;", cls=f"fa fa-{icons[sub.result]}"),
                h.span(verdict_name[sub.result])
            ),
            onclick=f"submissionPopupContestant('{sub.id}')"
        )

class SubmissionTable(UIElement):
    def __init__(self, subs):
        self.html = h.table(
            h.thead(
                h.tr(
                    h.th("Problem"),
                    h.th("Time"),
                    h.th("Language"),
                    h.th("Result")
                )
            ),
            h.tbody(
                *map(lambda sub: SubmissionRow(sub), subs)
            ),
            id="mySubmissions"
        )

class SubmissionCard(UIElement):
    def __init__(self, submission: Submission):
        subTime = submission.timestamp
        probName = submission.problem.title
        cls = "red" if submission.result != "ok" else ""
        self.html = div(cls="modal-content", contents=[
            div(cls=f"modal-header {cls}", contents=[
                h.h5(
                    f"Submission to {probName} at ",
                    h.span(subTime, cls="time-format")
                ),
                """
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>"""
            ]),
            div(cls="modal-body", contents=[
                h.strong("Language: <span class='language-format'>{}</span>".format(submission.language)),
                # h.br(),
                # h.strong("Result: ",
                #     h.select(cls=f"result-choice {submission.id}", onchange=f"changeSubmissionResult('{submission.id}')", contents=[
                #         *resultOptions(submission.result)
                #     ])
                # ),
                # h.br(),
                # h.br(),
                # h.button("Rejudge", type="button", onclick=f"rejudge('{submission.id}')", cls="btn btn-primary rejudge"),
                h.br(),
                h.br(),
                h.strong("Code:"),
                h.code(submission.code.replace("\n", "<br/>").replace(" ", "&nbsp;"), cls="code"),
                # div(cls="result-tabs", id="result-tabs", contents=[
                #     h.ul(*map(lambda x: TestCaseTab(x, submission), enumerate(submission.results))),
                #     *map(lambda x: TestCaseData(x, submission), zip(range(submission.problem.tests), submission.inputs, submission.outputs, submission.errors, submission.answers))
                # ])
            ])
        ])

def getSubmissions(params, user):
    submissions = []
    
    cont = Contest.getCurrent()
    if not cont:
        return ""
    
    Submission.forEach(lambda x: submissions.append(x) if x.user.id == user.id and cont.start <= x.timestamp <= cont.end else None)
    if len(submissions) == 0:
        return Page(
            h2("No Submissions Yet", cls="page-title"),
        )
    return Page(
        h2("Your Submissions", cls="page-title"),
        SubmissionTable(submissions)
    )

def contestant_submission(params, user):
    return SubmissionCard(Submission.get(params[0]))

register.web("/submissions", "loggedin", getSubmissions)
register.web("/contestantSubmission/([a-zA-Z0-9-]*)", "admin", contestant_submission)
